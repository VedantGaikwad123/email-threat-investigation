# Email Threat Investigation & Analysis Forensic Report

**Case File:** CA-ETI-01  
**Target Organization:** Solvex Industries Pvt. Ltd.  
**Investigating Target Mailbox:** Mr. Aditya Rao (Senior Finance Executive — `aditya.rao@solvexindustries.com`)  
**Investigator:** Lead Cyber Security & Threat Intelligence Analyst (Cryptonic Area Program)  
**Date of Report:** July 25, 2026  
**Classification:** CONFIDENTIAL / TLP:AMBER  

---

## 1. Executive Summary

Following reports of unusual mailbox activity and a suspected financial fraud attempt targeting the Finance Department of **Solvex Industries Pvt. Ltd.**, a forensic investigation was conducted on **13 recovered emails** from the inbox of **Mr. Aditya Rao, Senior Finance Executive**.

Each email underwent complete technical header dissection (SPF, DKIM, DMARC, TLS encryption, IP routing), social engineering analysis, attachment payload evaluation, and URL domain verification.

### Key Investigation Metrics

```mermaid
pie title Classification Breakdown across 13 Recovered Emails
    "SAFE / Genuine (5 Emails)" : 38.5
    "MEDIUM RISK / Suspicious (2 Emails)" : 15.4
    "SUSPICIOUS / Malicious (6 Emails)" : 46.1
```

| Metric | Count | Percentage | Key Findings |
| :--- | :--- | :--- | :--- |
| **Total Emails Analyzed** | 13 | 100% | Full mailbox audit completed |
| **SAFE / Legitimate Emails** | 5 | 38.5% | Genuine internal communications & verified vendor invoices |
| **MEDIUM RISK / Fraud Threat** | 2 | 15.4% | Vendor account compromise & unsolicited PII harvesting lure |
| **SUSPICIOUS / Malicious Threats** | 6 | 46.1% | Active phishing, BEC wire fraud, gift card scams & weaponized macros |
| **DMARC / SPF Failures** | 6 | 46.1% | Outbound domain spoofing & unauthenticated relays |
| **Unique Extracted IOCs** | 22 | — | Blocked on enterprise perimeter controls |

---

## 2. Risk Classification Rubric

All 13 emails were categorized into three distinct security tiers based on evidence:

| Classification | Technical & Threat Criteria | Operational Action Required |
| :--- | :--- | :--- |
| **SAFE** | Valid SPF, DKIM, and DMARC pass; legitimate IP origin; no mismatched links; valid business context. | No action required. Allow delivery. |
| **MEDIUM RISK** | Valid authentication but anomalous behavior (e.g. `Reply-To` mismatch, unexpected bank change request, unverified PII collection request). | Verify out-of-band via phone before taking any financial or data action. |
| **SUSPICIOUS / MALICIOUS** | Failed email authentication, typosquatting domains, credential harvesting URLs, executive BEC fraud, or macro-enabled attachments. | Block domain/IP on SEG & Firewall, purge email from inboxes, reset compromised credentials. |

---

## 3. Email-by-Email Analysis (13 Recovered Evidence Cases)

### Email 01 / 13 — Password Expiry Reminder
- **Subject:** `Password Expiry Reminder – Action Needed Within 5 Days`
- **Claimed Sender:** `IT Helpdesk – Solvex Industries <ithelpdesk@solvexindustries.com>`
- **Header Forensics:**
  - `From`: `ithelpdesk@solvexindustries.com`
  - `Reply-To`: `ithelpdesk@solvexindustries.com`
  - `Return-Path`: `ithelpdesk@solvexindustries.com`
  - `Received From`: `mail.solvexindustries.com (192.168.14.22)` [Internal Corporate Subnet]
  - `Authentication`: SPF: **PASS** | DKIM: **PASS** | DMARC: **PASS** | TLS: Yes (TLS 1.3)
- **Content & Link Analysis:** Automated password expiration notification (90-day policy). Directs user to log into the internal IT Service Portal manually from desktop or VPN. Contains **no hyperlinks** or attachments. Includes legitimate Helpdesk extension 204. Explicitly warns: *"Do not share your password with anyone, including IT staff."*
- **Classification:** **SAFE**
- **Reasoning:** Authenticated internal server origin, clean headers, standard IT hygiene practices, zero malicious links or attachments.

---

### Email 02 / 13 — Mailbox Storage Full Suspension Lure
- **Subject:** `URGENT: Your Mailbox Storage is FULL – Verify Now to Avoid Suspension`
- **Claimed Sender:** `IT Support Desk <support@solvex-industries-helpdesk.com>`
- **Header Forensics:**
  - `From`: `support@solvex-industries-helpdesk.com` (Fake domain: `solvex-industries-helpdesk.com`)
  - `Reply-To`: `recovery-team@mail-secure-verify.net` (External redirection)
  - `Return-Path`: `bounce@mail-secure-verify.net`
  - `Received From`: `unknown-host-193.41.77.108.static-cloud.ru (193.41.77.108)` [Russian Cloud IP]
  - `Authentication`: SPF: **FAIL** | DKIM: **FAIL** | DMARC: **FAIL** | TLS: No (Unencrypted)
- **Social Engineering & Link Analysis:** Uses psychological pressure (24-hour deadline, loss of 5GB mailbox data). Embedded link: `hxxp://solvex-industries-helpdesk.verify-account-secure.com/mailbox/confirm?user=aditya.rao`.
- **Classification:** **SUSPICIOUS / MALICIOUS**
- **Potential Impact:** Credential theft / M365 account takeover if credentials are entered on the fake phishing landing page.
- **Recommended Action:** Block domain `solvex-industries-helpdesk.com` and IP `193.41.77.108` on email gateway. Delete email immediately.

---

### Email 03 / 13 — Invoice SI-4471 & Bank Account Change Request
- **Subject:** `Invoice SI-4471 & Updated Bank Details for Future Payments`
- **Claimed Sender:** `Ramesh Kulkarni – Accounts, Apex Steel Traders <ramesh.kulkarni@apex-steeltraders.co>`
- **Header Forensics:**
  - `From`: `ramesh.kulkarni@apex-steeltraders.co`
  - `Reply-To`: `accounts.payments@apexsteel-billing.com` (Mismatched external domain)
  - `Return-Path`: `ramesh.kulkarni@apex-steeltraders.co`
  - `Received From`: `mail.apex-steeltraders.co (103.22.8.190)`
  - `Authentication`: SPF: **PASS** | DKIM: **PASS** | DMARC: **PASS** | TLS: Yes (TLS 1.2)
- **Threat & Content Analysis:** Involves an invoice for steel coils (Rs. 4,85,600/-). Claims their current account is restricted due to audit, requesting payments to a **NEW bank account**. The `Reply-To` field redirects to `apexsteel-billing.com`.
- **Classification:** **MEDIUM RISK**
- **Potential Impact:** High risk of financial fraud (Vendor Account Compromise / Payment Redirection Scam).
- **Recommended Action:** **DO NOT PAY to the new account.** Perform mandatory out-of-band verification by calling Ramesh Kulkarni on his pre-established official phone number before releasing funds.

---

### Email 04 / 13 — Revised Leave & Work-From-Home Policy
- **Subject:** `Revised Leave & Work-From-Home Policy – Effective 15 July 2026`
- **Claimed Sender:** `Human Resources – Solvex Industries <hr@solvexindustries.com>`
- **Header Forensics:**
  - `From`: `hr@solvexindustries.com`
  - `Reply-To`: `hr@solvexindustries.com`
  - `Return-Path`: `hr@solvexindustries.com`
  - `Received From`: `mail.solvexindustries.com (192.168.14.19)` [Internal Corporate IP]
  - `Authentication`: SPF: **PASS** | DKIM: **PASS** | DMARC: **PASS** | TLS: Yes (TLS 1.3)
- **Content Analysis:** Informs all employees of an increase in casual leave (8 to 10 days) and hybrid WFH options. Directs staff to the internal HR Portal. Contains no external links or attachments.
- **Classification:** **SAFE**
- **Reasoning:** 100% authenticated internal corporate email originating from internal mail server.

---

### Email 05 / 13 — Confidential Wire Transfer Request (CEO Fraud / BEC)
- **Subject:** `Confidential – Immediate Wire Transfer Required (Time Sensitive)`
- **Claimed Sender:** `Rajeev Malhotra (Managing Director) <rajeev.malhotra.md@gmail-corpmail.com>`
- **Header Forensics:**
  - `From`: `rajeev.malhotra.md@gmail-corpmail.com` (Fake consumer lookalike domain)
  - `Reply-To`: `rajeev.malhotra.md@gmail-corpmail.com`
  - `Received From`: `smtp-relay-88.freemailhost.io (45.137.22.9, Netherlands)`
  - `Authentication`: SPF: **NONE** | DKIM: **NONE** | DMARC: **NONE** | TLS: No
- **Social Engineering Analysis:** Classic Business Email Compromise (BEC). Impersonates MD Rajeev Malhotra. Demands urgent international wire transfer of **USD 18,500** for a "confidential acquisition". Exploits authority and secrecy ("Do not discuss this with Priya or anyone in Accounts").
- **Classification:** **SUSPICIOUS / MALICIOUS**
- **Potential Impact:** Direct financial loss of USD 18,500 via fraudulent wire transfer.
- **Recommended Action:** Block domain `gmail-corpmail.com` and relay IP `45.137.22.9`. Report attempt to CISO and Incident Response team.

---

### Email 06 / 13 — Google Drive File Sharing Notice
- **Subject:** `'Q1_Vendor_Compliance_Report.xlsx' has been shared with you`
- **Claimed Sender:** `Google Drive <drive-shares-noreply@google.com>`
- **Header Forensics:**
  - `From`: `drive-shares-noreply@google.com`
  - `Received From`: `mail-sor-f89.google.com (209.85.220.89)`
  - `Authentication`: SPF: **PASS** | DKIM: **PASS** | DMARC: **PASS** | TLS: Yes (TLS 1.3)
- **Content Analysis:** Authentic Google Drive notification. Includes personal note from colleague `priya.menon@solvexindustries.com` requesting review of vendor compliance spreadsheet for Friday audit call. Link points strictly to `https://docs.google.com/spreadsheets/...`.
- **Classification:** **SAFE**
- **Reasoning:** Fully authenticated message from official Google infrastructure matching legitimate work context.

---

### Email 07 / 13 — Unusual Sign-in Activity (Microsoft Account Phishing)
- **Subject:** `Unusual sign-in activity detected on your Microsoft account`
- **Claimed Sender:** `Microsoft account team <security-noreply@micros0ft-online.com>`
- **Header Forensics:**
  - `From`: `security-noreply@micros0ft-online.com` (Homoglyph typosquatting: `micros0ft` with zero)
  - `Reply-To`: `no-reply@micros0ft-online.com`
  - `Return-Path`: `bounce@micros0ft-online.com`
  - `Received From`: `host-77-91-134-6.vpn-exit.net (77.91.134.6, unknown origin)`
  - `Authentication`: SPF: **FAIL** | DKIM: **FAIL** | DMARC: **FAIL** | TLS: No
- **Social Engineering & Link Analysis:** Frightening alert claiming sign-in from Lagos, Nigeria. Demands identity verification within 12 hours. Embedded link: `hxxp://login.micros0ft-online.com/secure/verify-identity?ref=aditya.rao`.
- **Classification:** **SUSPICIOUS / MALICIOUS**
- **Potential Impact:** Corporate M365 credential theft and subsequent tenant breach.
- **Recommended Action:** Block domain `micros0ft-online.com` and IP `77.91.134.6`. Report phishing attempt to SOC.

---

### Email 08 / 13 — Executive Recruitment Lure & PII Collection Request
- **Subject:** `Exciting Career Opportunity – Senior Finance Role (Immediate Response Needed)`
- **Claimed Sender:** `Neha Kapoor, HR Consultant <neha.kapoor.hr@talentbridge-recruiters.net>`
- **Header Forensics:**
  - `From`: `neha.kapoor.hr@talentbridge-recruiters.net`
  - `Received From`: `mail.talentbridge-recruiters.net (156.213.44.71, Singapore)`
  - `Authentication`: SPF: **PASS** | DKIM: **PASS** | DMARC: **NONE** | TLS: Yes (TLS 1.2)
- **Threat & Attachment Analysis:** Unsolicited headhunter lure offering 40% salary hike. Asks recipient to send scanned copies of **latest salary slip and PAN card** within 24 hours. Attaches `JD_SeniorFinanceManager_Client.zip` (2.4MB archive).
- **Classification:** **MEDIUM RISK**
- **Potential Impact:** High risk of Identity Theft / Sensitive PII exfiltration, and potential malware execution if the ZIP file contains an executable dropper.
- **Recommended Action:** Do not reply or send PII. Sandbox and scan `JD_SeniorFinanceManager_Client.zip` in an isolated environment before opening.

---

### Email 09 / 13 — TallyPrime Cloud Subscription Renewal Invoice
- **Subject:** `Your TallyPrime Cloud Subscription Renewal Invoice – INV-88213`
- **Claimed Sender:** `Tally Solutions Billing <billing@tallysolutions.com>`
- **Header Forensics:**
  - `From`: `billing@tallysolutions.com`
  - `Received From`: `mta-out.tallysolutions.com (203.0.113.44)`
  - `Authentication`: SPF: **PASS** | DKIM: **PASS** | DMARC: **PASS** | TLS: Yes (TLS 1.3)
- **Content & Attachment Analysis:** Renewal invoice for TallyPrime Cloud (Rs. 32,500/-). Attachment `INV-88213_TallyPrime_Renewal.pdf` (146KB). Explicitly notes: *"Payments can be made through your existing registered payment method... no bank details have changed."*
- **Classification:** **SAFE**
- **Reasoning:** Genuine vendor communication, fully authenticated headers, zero bank redirection anomalies.

---

### Email 10 / 13 — International Email Lottery Scam (Advance-Fee Fraud)
- **Subject:** `CONGRATULATIONS!!! YOU HAVE WON USD 1,000,000 IN THE INTERNATIONAL EMAIL LOTTERY`
- **Claimed Sender:** `INTERNATIONAL LOTTERY BOARD <claims.department009@yandex-mailer.com>`
- **Header Forensics:**
  - `From`: `claims.department009@yandex-mailer.com`
  - `Reply-To`: `agent.williams.claims@outlook-verify.info` (External redirection)
  - `Received From`: `unknown-relay-node4.freehosting-mail.com (185.220.101.44, Netherlands)`
  - `Authentication`: SPF: **FAIL** | DKIM: **FAIL** | DMARC: **FAIL** | TLS: No
- **Threat & Link Analysis:** Classic 419 / Advance-Fee Scam claiming USD 1,000,000 win. Demands USD 250 processing fee and personal ID copy within 48 hours. Link: `hxxp://claim-your-prize-now.lottery-verify.info/claim?ref=44921`.
- **Classification:** **SUSPICIOUS / MALICIOUS**
- **Potential Impact:** Advance-fee financial loss (USD 250) and identity theft.
- **Recommended Action:** Block `yandex-mailer.com`, `outlook-verify.info`, `lottery-verify.info`, and IP `185.220.101.44`. Mark as spam.

---

### Email 11 / 13 — Amazon Gift Card Request (CFO Impersonation BEC)
- **Subject:** `Quick request before my flight`
- **Claimed Sender:** `Suresh Iyer (CFO) <suresh.iyer@solvexindustries.com>`
- **Header Forensics:**
  - `From`: `suresh.iyer@solvexindustries.com`
  - `Reply-To`: `s.iyer.cfo.travel@outlook.com` (External Outlook hijacking)
  - `Received From`: `mail.solvexindustries.com (192.168.14.19)`
  - `Authentication`: SPF: **PASS** (Envelope sender matched) | DKIM: **PASS** | DMARC: **PASS**
- **Threat & Social Engineering Analysis:** Impersonates CFO Suresh Iyer claiming his corporate card failed at airport lounge. Asks Aditya to buy **5 Amazon gift cards of Rs. 5,000 each (Rs. 25,000 total)** and email codes within 20 minutes. Explicitly forbids phone calls: *"Please don't call the office landline about this, my phone network is patchy."*
- **Classification:** **SUSPICIOUS / MALICIOUS**
- **Potential Impact:** Financial loss of Rs. 25,000 via untraceable gift card codes.
- **Recommended Action:** **DO NOT PURCHASE GIFT CARDS.** Report `Reply-To` domain `s.iyer.cfo.travel@outlook.com` to security team. Contact CFO directly on his verified mobile number.

---

### Email 12 / 13 — Mandatory Q3 Security Awareness Training
- **Subject:** `Reminder: Mandatory Security Awareness Training – Due This Friday`
- **Claimed Sender:** `Information Security Team – Solvex Industries <infosec@solvexindustries.com>`
- **Header Forensics:**
  - `From`: `infosec@solvexindustries.com`
  - `Received From`: `mail.solvexindustries.com (192.168.14.19)` [Internal Corporate IP]
  - `Authentication`: SPF: **PASS** | DKIM: **PASS** | DMARC: **PASS** | TLS: Yes (TLS 1.3)
- **Content Analysis:** Standard reminder for Q3 Security Awareness Training due Friday, 17 July 2026. Directs staff to `learn.solvexindustries.com`. Contains no external links or attachments.
- **Classification:** **SAFE**
- **Reasoning:** 100% authenticated internal corporate email.

---

### Email 13 / 13 — Pending Transport Invoice (Macro Ransomware Dropper)
- **Subject:** `Pending Invoice – Please Review & Process on Priority`
- **Claimed Sender:** `Accounts Receivable <accounts.receivable@shreeganesh-logistics.in>`
- **Header Forensics:**
  - `From`: `accounts.receivable@shreeganesh-logistics.in`
  - `Received From`: `webmail-host-4.sharedhosting-cluster.com (41.203.88.17)` [Unrelated hosting IP]
  - `Authentication`: SPF: **FAIL** (Unauthorized domain) | DKIM: **NONE** | DMARC: **FAIL** | TLS: No
- **Threat & Payload Analysis:** Claims overdue transport invoice for Pune warehouse. Explicitly instructs: *"Please enable editing/macros if prompted so all the invoice tables display correctly."* Attaches macro-enabled Word document `Pending_Invoice_Challan_Details.docm` (1.1MB) and includes phishing link `hxxp://shreeganesh-logistics.in.invoice-view-secure.com/download?file=inv2207`.
- **Classification:** **SUSPICIOUS / MALICIOUS**
- **Potential Impact:** Malicious VBA macro execution leading to Trojan downloader / Ransomware infection on endpoint.
- **Recommended Action:** Block domain `shreeganesh-logistics.in.invoice-view-secure.com` and IP `41.203.88.17`. Quarantine `.docm` attachment across all mailboxes.

---

## 4. Master Indicator of Compromise (IOC) Database

All extracted malicious indicators from Case File CA-ETI-01 have been compiled below for integration into perimeter firewalls, SIEM, and EDR blocklists:

| IOC Type | Indicator Value / Hash | Associated Threat | Source Email | Action Required |
| :--- | :--- | :--- | :--- | :--- |
| **Domain** | `solvex-industries-helpdesk.com` | Typosquat Phishing | Email 02 | SEG & DNS Block |
| **Domain** | `mail-secure-verify.net` | Phishing Infrastructure | Email 02 | Firewall Block |
| **Domain** | `gmail-corpmail.com` | CEO Fraud Domain | Email 05 | SEG Block |
| **Domain** | `micros0ft-online.com` | Microsoft Typosquat | Email 07 | DNS Sinkhole |
| **Domain** | `lottery-verify.info` | Advance-Fee Scam | Email 10 | Web Gateway Block |
| **Domain** | `outlook-verify.info` | Phishing Reply-To | Email 10 | SEG Block |
| **Domain** | `s.iyer.cfo.travel@outlook.com` | BEC Reply-To Hijack | Email 11 | Mail Filter Rule |
| **Domain** | `shreeganesh-logistics.in.invoice-view-secure.com` | Macro Dropper Host | Email 13 | Proxy & DNS Block |
| **IPv4** | `193.41.77.108` | Russian Phishing Relay | Email 02 | Perimeter Firewall DROP |
| **IPv4** | `45.137.22.9` | Netherlands BEC Host | Email 05 | Perimeter Firewall DROP |
| **IPv4** | `77.91.134.6` | VPN Exit Node / Phishing | Email 07 | Perimeter Firewall DROP |
| **IPv4** | `185.220.101.44` | Netherlands Scam Relay | Email 10 | Perimeter Firewall DROP |
| **IPv4** | `41.203.88.17` | Malicious Hosting Cluster | Email 13 | Perimeter Firewall DROP |
| **Filename** | `Pending_Invoice_Challan_Details.docm` | VBA Ransomware Dropper | Email 13 | EDR Signature Block |
| **Filename** | `JD_SeniorFinanceManager_Client.zip` | Suspicious Archive | Email 08 | Gateway Quarantine |

---

## 5. Strategic Recommendations & Employee Guidance

### 5.1 Immediate Employee Actions for Mr. Aditya Rao
1. **Never Enable Macros:** Do not enable macros on Word/Excel documents received via email (especially Email 13).
2. **Mandatory Out-of-Band Financial Verification:** For any request to change bank accounts (Email 03) or perform urgent wire transfers (Email 05), call the sender on their known internal extension before acting.
3. **Ignore Gift Card Requests:** C-level executives will never ask employees to purchase gift cards via email (Email 11).
4. **Do Not Share PII with Unverified Recruiters:** Avoid sending PAN card and salary slips to unverified external emails (Email 08).

### 5.2 Enterprise Technical Controls
1. **Harden DMARC to `p=reject`:** Enforce `p=reject` on `solvexindustries.com` to prevent external domain spoofing.
2. **Inbound Reply-To Mismatch Inspection:** Configure SEG to flag emails where the `Reply-To` domain differs from the `From` header domain (Email 03 & Email 11).
3. **Block Macro-Enabled Attachments (`.docm`, `.xlsm`):** Quarantine all inbound macro-enabled attachments at the email boundary.
4. **Deploy FIDO2 Hardware Security Keys:** Mandate WebAuthn FIDO2 keys for M365 access to render typosquatting phishing links (Email 02 & Email 07) ineffective.

---

**Report Sign-Off:**  
*Lead Cyber Security & Threat Intelligence Analyst*  
*Cryptonic Area Cybersecurity Internship Program*  
