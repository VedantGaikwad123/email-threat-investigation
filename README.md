# 📧 Email Threat Investigation & Analysis — SOC Project

A complete, end-to-end **Security Operations Center (SOC) email threat investigation** covering forensic header analysis, IOC extraction, OSINT verification, risk classification, and automated Python tooling for parsing raw `.eml` artifacts.

---

## 🗂️ Project Structure

```
email-threat-investigation/
├── emails.pdf                             # Original case briefing document (Cryptonic Area)
├── email_threat_investigation_plan.md     # Operational methodology & phase-by-phase blueprint
├── email_threat_investigation_report.md   # Full forensic investigation report (13 email cases)
├── PROJECT_REPORT.md                      # Executive project completion report
├── soc_email_parser.py                    # 🐍 Automated EML header & IOC extractor tool
├── generate_sample_emails.py              # 🐍 Synthetic .eml test file generator
├── parsed_iocs.json                       # Automated JSON output from parser
└── sample_emails/                         # 13 synthetic .eml evidence artifacts
    ├── Email_01.eml                       # IT Helpdesk — Password Expiry Reminder (SAFE)
    ├── Email_02.eml                       # Mailbox Full Suspension Lure (SUSPICIOUS)
    ├── Email_03.eml                       # Invoice Bank Account Change (MEDIUM RISK)
    ├── Email_04.eml                       # Revised Leave & WFH Policy (SAFE)
    ├── Email_05.eml                       # CEO Wire Transfer Fraud / BEC (SUSPICIOUS)
    ├── Email_06.eml                       # Google Drive Share Notice (SAFE)
    ├── Email_07.eml                       # Microsoft Phishing / Homoglyph (SUSPICIOUS)
    ├── Email_08.eml                       # Recruiter PII Harvesting Lure (MEDIUM RISK)
    ├── Email_09.eml                       # TallyPrime Renewal Invoice (SAFE)
    ├── Email_10.eml                       # Advance-Fee / 419 Lottery Scam (SUSPICIOUS)
    ├── Email_11.eml                       # CFO Amazon Gift Card Scam (SUSPICIOUS)
    ├── Email_12.eml                       # Mandatory Security Training (SAFE)
    └── Email_13.eml                       # Macro Dropper Invoice (.docm) (SUSPICIOUS)
```

---

## ⚡ Quick Start

### Prerequisites

- **Python 3.8+** (Standard library only — no third-party packages required)
- **Git** (for cloning)

Verify Python is installed:
```bash
python --version
```

### 1. Clone the Repository

```bash
git clone https://github.com/VedantGaikwad123/email-threat-investigation.git
cd email-threat-investigation
```

### 2. Generate the 13 Sample `.eml` Test Artifacts

```bash
python generate_sample_emails.py
```

This creates `sample_emails/Email_01.eml` through `Email_13.eml` — synthetic `.eml` files representing all 13 email cases from Case File CA-ETI-01. Attachments are inert placeholder bytes (no real malicious code is shipped).

### 3. Run the SOC Parser Against All 13 Emails

```bash
python soc_email_parser.py --dir sample_emails --output parsed_iocs.json
```

This produces a consolidated `parsed_iocs.json` containing extracted headers, links, attachments, and SHA-256 hashes for every email in the directory.

### 4. Parse a Single `.eml` File

```bash
python soc_email_parser.py --eml sample_emails/Email_05.eml --output ceo_fraud_iocs.json
```

---

## 🛠️ Tool Reference — `soc_email_parser.py`

The core SOC automation tool. Parses raw `.eml` files and extracts threat intelligence artifacts into structured JSON.

### What It Extracts

| Artifact | Field / Data |
| :--- | :--- |
| **Email Headers** | From, To, Reply-To, Return-Path, Date, Subject, Message-ID, Authentication-Results |
| **Authentication** | SPF / DKIM / DMARC pass/fail status from `Authentication-Results` header |
| **Hyperlinks** | All URLs from body (plain-text and HTML), cleaned of trailing punctuation |
| **IP Addresses** | Public IPs extracted from headers and body (RFC1918 private IPs filtered out) |
| **Domains** | Extracted from all parsed URLs |
| **Attachments** | Filename, content-type, size in bytes, SHA-256 hash, high-risk extension flag |

### CLI Arguments

```
usage: soc_email_parser.py [-h] [--eml EML] [--dir DIR] [--output OUTPUT]

options:
  --eml    PATH    Path to a single .eml file to analyze
  --dir    PATH    Path to a directory containing multiple .eml files
  --output FILE    Output JSON file path (default: analysis_output.json)
```

### Sample JSON Output (truncated)

```json
{
  "file": "Email_05.eml",
  "headers": {
    "From": "Rajeev Malhotra (MD) <rajeev.malhotra.md@gmail-corpmail.com>",
    "Reply-To": "rajeev.malhotra.md@gmail-corpmail.com",
    "Subject": "Confidential – Immediate Wire Transfer Required (Time Sensitive)",
    "Authentication-Results": "spf=none; dkim=none; dmarc=none"
  },
  "attachments": [],
  "extracted_links": [],
  "iocs": {
    "ips": [],
    "domains": [],
    "urls": [],
    "hashes": []
  }
}
```

---

## 🔬 Investigation Methodology

The investigation follows a rigorous **5-phase SOC process** aligned with NIST SP 800-61 r2:

```
Phase 0 → Safety Setup & Working File Preparation
Phase 1 → Per-Email Header Forensics, Content & Link Analysis
Phase 2 → IOC Extraction & Deduplication
Phase 3 → OSINT Cross-Verification (VirusTotal / urlscan.io / MXToolbox / AbuseIPDB)
Phase 4 → Risk Classification (SAFE / MEDIUM RISK / SUSPICIOUS)
Phase 5 → Remediation Playbook & Incident Response Actions
```

Full methodology details: [email_threat_investigation_plan.md](email_threat_investigation_plan.md)

---

## 📊 Case File CA-ETI-01 — Key Findings

| Metric | Value |
| :--- | :--- |
| **Total Emails Analyzed** | 13 |
| **SAFE / Legitimate** | 5 (38.5%) |
| **MEDIUM RISK / Suspicious** | 2 (15.4%) |
| **SUSPICIOUS / Malicious** | 6 (46.1%) |
| **DMARC Failures** | 6 (46.1%) |
| **Unique IOCs Extracted** | 14+ Domains, IPs, Filenames, Hashes |

### Attack Vectors Investigated

| # | Email | Attack Technique | Classification |
| :--- | :--- | :--- | :--- |
| 01 | IT Helpdesk — Password Expiry Reminder | — | ✅ SAFE |
| 02 | Mailbox Storage Full | Credential Phishing / Typosquatting | 🔴 SUSPICIOUS |
| 03 | Invoice SI-4471 + Bank Change | Vendor Account Compromise | 🟡 MEDIUM |
| 04 | Revised Leave & WFH Policy | — | ✅ SAFE |
| 05 | MD Wire Transfer Request | Business Email Compromise (BEC) | 🔴 SUSPICIOUS |
| 06 | Google Drive Share | — | ✅ SAFE |
| 07 | Microsoft Unusual Sign-in | Homoglyph Typosquatting + Phishing | 🔴 SUSPICIOUS |
| 08 | Senior Finance Recruiter | PII Harvesting / Social Engineering | 🟡 MEDIUM |
| 09 | TallyPrime Renewal Invoice | — | ✅ SAFE |
| 10 | USD 1M Lottery Win | Advance-Fee / 419 Fraud | 🔴 SUSPICIOUS |
| 11 | CFO Gift Card Request | Gift Card BEC Fraud | 🔴 SUSPICIOUS |
| 12 | Security Awareness Training | — | ✅ SAFE |
| 13 | Pending Transport Invoice | VBA Macro Dropper (.docm) | 🔴 SUSPICIOUS |

Full detailed evidence write-ups: [email_threat_investigation_report.md](email_threat_investigation_report.md)

---

## 🛡️ Safety Notice

> All `.eml` files in `sample_emails/` are **synthetic test artifacts**. Attachment payloads are inert placeholder bytes — no real malware, shellcode, or macros are present in any file in this repository.
>
> Never open, click, or execute any URLs, domains, or file hashes cited in the investigation report outside of an isolated sandbox environment (e.g., VirusTotal, urlscan.io, Any.run).

---

## 📦 Dependencies

This project uses **Python standard library only** — no `pip install` required.

```
# requirements.txt
# Standard library only — no third-party packages required.
# Compatible with Python 3.8+
```

Modules used internally: `email`, `os`, `re`, `json`, `hashlib`, `argparse`, `urllib.parse`

---

## 📁 Key Output Files

| File | Description |
| :--- | :--- |
| `parsed_iocs.json` | Consolidated JSON output of all extracted IOCs from 13 emails |
| `email_threat_investigation_report.md` | Full SOC forensic report (headers, evidence, OSINT, remediation) |
| `PROJECT_REPORT.md` | Executive summary & internship submission document |

---

## 👤 Author

**Vedant Gaikwad**  
GitHub: [@VedantGaikwad123](https://github.com/VedantGaikwad123)

---

