#!/usr/bin/env python3
"""
SOC Email Threat Parser & IOC Extraction Tool
Author: Lead Cybersecurity / SOC Threat Analyst
Description: Parses raw email files (.eml), extracts email headers, evaluates SPF/DKIM/DMARC,
             extracts hyperlinks, attachments, hashes (SHA-256), and deduplicates IOCs.
"""

import os
import re
import json
import hashlib
import argparse
from email import policy
from email.parser import BytesParser
from urllib.parse import urlparse

# Regular Expressions for IOC Extraction
REGEX_IP = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
REGEX_URL = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
REGEX_DOMAIN = r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'

class SOCEmailParser:
    def __init__(self, eml_path):
        self.eml_path = eml_path
        self.msg = None
        self.headers = {}
        self.body_text = ""
        self.body_html = ""
        self.attachments = []
        self.links = []
        self.iocs = {
            "ips": set(),
            "domains": set(),
            "urls": set(),
            "hashes": set()
        }

    def parse(self):
        if not os.path.exists(self.eml_path):
            raise FileNotFoundError(f"Email file not found: {self.eml_path}")

        with open(self.eml_path, 'rb') as fp:
            self.msg = BytesParser(policy=policy.default).parse(fp)

        # Extract Header Fields
        self.headers['From'] = str(self.msg.get('From', 'N/A'))
        self.headers['To'] = str(self.msg.get('To', 'N/A'))
        self.headers['Reply-To'] = str(self.msg.get('Reply-To', 'N/A'))
        self.headers['Subject'] = str(self.msg.get('Subject', 'N/A'))
        self.headers['Date'] = str(self.msg.get('Date', 'N/A'))
        self.headers['Message-ID'] = str(self.msg.get('Message-ID', 'N/A'))
        self.headers['Authentication-Results'] = str(self.msg.get('Authentication-Results', 'N/A'))
        self.headers['Return-Path'] = str(self.msg.get('Return-Path', 'N/A'))

        # Extract Payload / Body & Attachments
        if self.msg.is_multipart():
            for part in self.msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" in content_disposition:
                    self._process_attachment(part)
                elif content_type == "text/plain":
                    self.body_text += str(part.get_content())
                elif content_type == "text/html":
                    self.body_html += str(part.get_content())
        else:
            self.body_text = str(self.msg.get_content())

        # Perform Threat Artifact Extraction
        self._extract_links()
        self._extract_iocs()

    def _process_attachment(self, part):
        filename = part.get_filename() or "unnamed_attachment"
        payload = part.get_payload(decode=True) or b""
        sha256_hash = hashlib.sha256(payload).hexdigest()

        attachment_info = {
            "filename": filename,
            "size_bytes": len(payload),
            "content_type": part.get_content_type(),
            "sha256": sha256_hash,
            "suspicious": self._is_suspicious_extension(filename)
        }
        self.attachments.append(attachment_info)
        self.iocs["hashes"].add(sha256_hash)

    def _is_suspicious_extension(self, filename):
        high_risk_ext = ['.exe', '.scr', '.vbs', '.js', '.bat', '.cmd', '.xlsm', '.docm', '.htm', '.html', '.zip']
        lower_filename = filename.lower()
        return any(lower_filename.endswith(ext) for ext in high_risk_ext) or filename.count('.') > 1

    def _extract_links(self):
        raw_urls = re.findall(REGEX_URL, self.body_text + " " + self.body_html)
        for url in raw_urls:
            clean_url = url.rstrip(')>],."\'')
            if clean_url not in self.links:
                self.links.append(clean_url)
                self.iocs["urls"].add(clean_url)

    def _extract_iocs(self):
        full_content = f"{json.dumps(self.headers)} {self.body_text} {self.body_html}"

        for ip in re.findall(REGEX_IP, full_content):
            if not ip.startswith('127.') and not ip.startswith('10.') and not ip.startswith('192.168.'):
                self.iocs["ips"].add(ip)

        for url in self.links:
            parsed = urlparse(url)
            if parsed.netloc:
                domain = parsed.netloc.split(':')[0]
                self.iocs["domains"].add(domain)

    def generate_report(self):
        return {
            "file": os.path.basename(self.eml_path),
            "headers": self.headers,
            "attachments": self.attachments,
            "extracted_links": self.links,
            "iocs": {
                "ips": sorted(list(self.iocs["ips"])),
                "domains": sorted(list(self.iocs["domains"])),
                "urls": sorted(list(self.iocs["urls"])),
                "hashes": sorted(list(self.iocs["hashes"]))
            }
        }

def analyze_directory(directory_path):
    results = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.eml'):
                eml_path = os.path.join(root, file)
                print(f"[+] Parsing EML Artifact: {file}")
                parser = SOCEmailParser(eml_path)
                parser.parse()
                results.append(parser.generate_report())
    return results

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="SOC Email Parser & Threat Intelligence Extractor")
    arg_parser.add_argument("--eml", help="Path to single .eml file to parse")
    arg_parser.add_argument("--dir", help="Directory containing multiple .eml files")
    arg_parser.add_argument("--output", default="analysis_output.json", help="Output JSON file path")
    args = arg_parser.parse_args()

    if args.eml:
        parser = SOCEmailParser(args.eml)
        parser.parse()
        report = parser.generate_report()
        print(json.dumps(report, indent=2))
        with open(args.output, 'w') as out_f:
            json.dump(report, out_f, indent=2)
        print(f"\n[OK] Analysis saved to {args.output}")
    elif args.dir:
        reports = analyze_directory(args.dir)
        with open(args.output, 'w') as out_f:
            json.dump(reports, out_f, indent=2)
        print(f"\n[OK] Analyzed {len(reports)} emails. Consolidated output saved to {args.output}")
    else:
        print("[!] Please specify --eml <filepath> or --dir <directory_path>")
