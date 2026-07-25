#!/usr/bin/env python3
"""
SOC Email Threat Parser & IOC Extraction Tool
Author: Lead Cybersecurity / SOC Threat Analyst
Version: 2.0 — Fixed critical attachment detection bypasses, Received IP extraction,
          proper private IP filtering, RTLO detection, CSV export, and verbose logging.
"""

import os
import re
import json
import csv
import hashlib
import logging
import argparse
import ipaddress
import unicodedata
from email import policy
from email.parser import BytesParser
from urllib.parse import urlparse

# ─── Regex Patterns ───────────────────────────────────────────────────────────
REGEX_IP  = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
REGEX_URL = r'https?://[^\s<>"]+|www\.[^\s<>"]+'

# High-risk file extensions for attachment flagging
HIGH_RISK_EXT = {
    '.exe', '.scr', '.vbs', '.js', '.bat', '.cmd', '.ps1',
    '.xlsm', '.docm', '.pptm', '.xlam', '.xltm', '.dotm',
    '.htm', '.html', '.hta', '.iso', '.img', '.zip', '.rar',
    '.7z', '.jar', '.wsf', '.msi', '.dll'
}

# Unicode Right-to-Left Override — used to spoof file extensions
RTLO_CHARS = {'\u202e', '\u200f', '\u202b', '\u2067'}

# Known legitimate internal domains (update per org)
KNOWN_GOOD_DOMAINS = {
    'solvexindustries.com', 'tallysolutions.com',
    'google.com', 'github.com', 'microsoft.com',
    'docs.google.com', 'drive.google.com'
}

# ─── Logger Setup ─────────────────────────────────────────────────────────────
def setup_logger(verbose: bool) -> logging.Logger:
    logger = logging.getLogger('soc_parser')
    handler = logging.StreamHandler()
    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)
    handler.setLevel(level)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


# ─── Core Parser Class ────────────────────────────────────────────────────────
class SOCEmailParser:
    def __init__(self, eml_path: str, logger: logging.Logger):
        self.eml_path = eml_path
        self.log = logger
        self.msg = None
        self.headers = {}
        self.body_text = ""
        self.body_html = ""
        self.received_raw = []
        self.attachments = []
        self.links = []
        self.iocs = {
            "ips": set(),
            "domains": set(),
            "urls": set(),
            "hashes": set(),
            "suspicious_filenames": set()
        }

    def parse(self):
        if not os.path.exists(self.eml_path):
            raise FileNotFoundError(f"Email file not found: {self.eml_path}")

        with open(self.eml_path, 'rb') as fp:
            self.msg = BytesParser(policy=policy.default).parse(fp)

        self.log.debug(f"Opened: {os.path.basename(self.eml_path)}")
        self._extract_headers()
        self._extract_body_and_attachments()
        self._extract_links()
        self._extract_iocs()

    # ── Header Extraction ──────────────────────────────────────────────────
    def _extract_headers(self):
        for field in ('From', 'To', 'Cc', 'Bcc', 'Reply-To', 'Return-Path',
                      'Subject', 'Date', 'Message-ID', 'Authentication-Results'):
            self.headers[field] = str(self.msg.get(field, 'N/A'))

        # Extract ALL Received headers (chain of mail hops)
        self.received_raw = [str(r) for r in self.msg.get_all('Received') or []]
        self.headers['Received'] = self.received_raw
        self.log.debug(f"  Headers extracted. Received hops: {len(self.received_raw)}")

    # ── Body & Attachment Extraction ───────────────────────────────────────
    def _extract_body_and_attachments(self):
        if self.msg.is_multipart():
            for part in self.msg.walk():
                content_type = part.get_content_type()
                filename = part.get_filename()  # Works for both Content-Disposition forms

                # FIX (Critical): Trigger on filename presence, not Content-Disposition value.
                # Catches: Content-Disposition: inline, Content-Type: name=, and standard attachments.
                if filename:
                    self.log.debug(f"  Attachment found: {filename}")
                    self._process_attachment(part, filename)
                elif content_type == 'text/plain':
                    self.body_text += str(part.get_content())
                elif content_type == 'text/html':
                    self.body_html += str(part.get_content())
        else:
            self.body_text = str(self.msg.get_content())

    def _process_attachment(self, part, filename: str):
        payload = part.get_payload(decode=True) or b""
        sha256_hash = hashlib.sha256(payload).hexdigest()
        extension = os.path.splitext(filename.lower())[-1]
        double_ext = filename.lower().count('.') > 1

        # FIX (Medium): Detect RTLO / Unicode bidirectional override in filenames
        has_rtlo = any(c in RTLO_CHARS for c in filename)
        has_control = any(unicodedata.category(c) == 'Cf' for c in filename)

        suspicious = (
            extension in HIGH_RISK_EXT
            or double_ext
            or has_rtlo
            or has_control
        )

        self.attachments.append({
            "filename": filename,
            "size_bytes": len(payload),
            "content_type": part.get_content_type(),
            "sha256": sha256_hash,
            "extension": extension,
            "double_extension": double_ext,
            "rtlo_detected": has_rtlo,
            "suspicious": suspicious
        })
        self.iocs["hashes"].add(sha256_hash)
        if suspicious:
            self.iocs["suspicious_filenames"].add(filename)
            self.log.debug(f"    [!] Suspicious attachment: {filename} (SHA256: {sha256_hash[:16]}...)")

    # ── Link Extraction ────────────────────────────────────────────────────
    def _extract_links(self):
        combined = self.body_text + " " + self.body_html
        for url in re.findall(REGEX_URL, combined):
            clean = url.rstrip(')>],."\'')
            if clean not in self.links:
                self.links.append(clean)
                self.iocs["urls"].add(clean)
                parsed = urlparse(clean)
                if parsed.netloc:
                    domain = parsed.netloc.split(':')[0].lower()
                    self.iocs["domains"].add(domain)
                    self.log.debug(f"  URL: {clean} → Domain: {domain}")

    # ── IP / IOC Extraction ────────────────────────────────────────────────
    def _extract_iocs(self):
        # Scan headers, body, AND Received chain for IPs
        scan_text = (
            json.dumps(self.headers)
            + " " + self.body_text
            + " " + self.body_html
            + " " + " ".join(self.received_raw)
        )

        for ip_str in re.findall(REGEX_IP, scan_text):
            try:
                # FIX (Medium): Use ipaddress module for complete RFC1918 + link-local filtering
                ip_obj = ipaddress.ip_address(ip_str)
                if not ip_obj.is_private and not ip_obj.is_loopback and not ip_obj.is_link_local:
                    self.iocs["ips"].add(ip_str)
                    self.log.debug(f"  Public IP found: {ip_str}")
            except ValueError:
                pass  # Not a valid IP

    # ── Report Generator ───────────────────────────────────────────────────
    def generate_report(self) -> dict:
        # Flag domains NOT in the known-good list
        external_domains = sorted([
            d for d in self.iocs["domains"]
            if not any(d.endswith(gd) for gd in KNOWN_GOOD_DOMAINS)
        ])

        return {
            "file": os.path.basename(self.eml_path),
            "headers": {k: v for k, v in self.headers.items() if k != 'Received'},
            "received_hops": self.received_raw,
            "attachments": self.attachments,
            "extracted_links": self.links,
            "iocs": {
                "ips": sorted(self.iocs["ips"]),
                "domains": sorted(self.iocs["domains"]),
                "external_unverified_domains": external_domains,
                "urls": sorted(self.iocs["urls"]),
                "hashes": sorted(self.iocs["hashes"]),
                "suspicious_filenames": sorted(self.iocs["suspicious_filenames"])
            }
        }


# ─── Directory Batch Analysis ─────────────────────────────────────────────────
def analyze_directory(directory_path: str, logger: logging.Logger) -> list:
    results = []
    eml_files = [f for f in os.listdir(directory_path) if f.endswith('.eml')]
    eml_files.sort()
    logger.info(f"Found {len(eml_files)} .eml file(s) in '{directory_path}'")

    for filename in eml_files:
        eml_path = os.path.join(directory_path, filename)
        logger.info(f"  Parsing: {filename}")
        parser = SOCEmailParser(eml_path, logger)
        parser.parse()
        results.append(parser.generate_report())

    return results


# ─── CSV Export ───────────────────────────────────────────────────────────────
def export_iocs_csv(reports: list, output_path: str, logger: logging.Logger):
    rows = []
    for report in reports:
        source = report['file']
        iocs = report['iocs']
        for ip in iocs['ips']:
            rows.append({'indicator': ip, 'type': 'IPv4', 'source_email': source, 'description': 'Public IP extracted from headers/body'})
        for domain in iocs['external_unverified_domains']:
            rows.append({'indicator': domain, 'type': 'Domain', 'source_email': source, 'description': 'External/unverified domain'})
        for url in iocs['urls']:
            rows.append({'indicator': url, 'type': 'URL', 'source_email': source, 'description': 'URL extracted from body'})
        for h in iocs['hashes']:
            rows.append({'indicator': h, 'type': 'SHA256', 'source_email': source, 'description': 'Attachment SHA-256 hash'})
        for fname in iocs['suspicious_filenames']:
            rows.append({'indicator': fname, 'type': 'Filename', 'source_email': source, 'description': 'Suspicious attachment filename'})

    if rows:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['indicator', 'type', 'source_email', 'description'])
            writer.writeheader()
            writer.writerows(rows)
        logger.info(f"CSV export saved → {output_path} ({len(rows)} IOC entries)")
    else:
        logger.info("No IOCs to export to CSV.")


# ─── CLI Entry Point ──────────────────────────────────────────────────────────
def main():
    arg_parser = argparse.ArgumentParser(
        description="SOC Email Threat Parser & IOC Extractor — v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Parse a single .eml file:
    python soc_email_parser.py --eml sample_emails/Email_05.eml --output ceo_fraud.json

  Parse all emails in a directory:
    python soc_email_parser.py --dir sample_emails --output parsed_iocs.json

  Parse directory, export IOCs to CSV, with verbose logging:
    python soc_email_parser.py --dir sample_emails --output parsed_iocs.json --export-csv iocs.csv -v
        """
    )
    arg_parser.add_argument('--eml',        help='Path to a single .eml file to analyze')
    arg_parser.add_argument('--dir',        help='Directory containing multiple .eml files')
    arg_parser.add_argument('--output',     default='analysis_output.json', help='Output JSON file (default: analysis_output.json)')
    arg_parser.add_argument('--export-csv', metavar='CSV_FILE', help='Export deduplicated IOC list as CSV')
    arg_parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose debug logging')
    args = arg_parser.parse_args()

    logger = setup_logger(args.verbose)

    if args.eml:
        parser = SOCEmailParser(args.eml, logger)
        parser.parse()
        report = parser.generate_report()
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        logger.info(f"Analysis complete → {args.output}")
        if args.export_csv:
            export_iocs_csv([report], args.export_csv, logger)

    elif args.dir:
        reports = analyze_directory(args.dir, logger)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(reports, f, indent=2)
        logger.info(f"Analyzed {len(reports)} email(s) → {args.output}")
        if args.export_csv:
            export_iocs_csv(reports, args.export_csv, logger)

    else:
        arg_parser.print_help()


if __name__ == '__main__':
    main()
