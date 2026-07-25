# Email Threat Investigation & Analysis — Full Development Plan

**Project:** SOC / Email Security Analyst Simulation
**Goal:** Investigate 10–12 sample emails, extract IOCs, classify risk, verify with OSINT, and produce a professional report.

---

## PHASE 0 — Preparation (Before You Analyze Anything)

### Step 0.1 — Download and Organize
- Download the PDF from the provided link.
- Do **not** open any embedded links or attachments from within the PDF viewer if it renders them as live objects — treat the PDF itself as a document to read, not to interact with.
- Extract each of the 10–12 emails into its own file or section (copy the raw text, headers, and any visible link/attachment info). Label them clearly: `Email_01`, `Email_02`, ... `Email_12`.

### Step 0.2 — Set Up Your Working Files
Create these before starting analysis so you're filling in structure as you go, not scrambling to build it at the end:

1. **Tracking Spreadsheet** (Excel/Sheets) with columns:
   - Email # | Sender Address | Display Name | Subject Line | Links Found | Attachments Found | Header Anomalies | Social Engineering Cues | Verdict | Risk Level | Verification Status

2. **IOC Master List** with columns:
   - IOC Value | IOC Type (domain / URL / IP / filename / hash) | Found In (Email #) | Why Suspicious | OSINT Tool Used | Verification Result | Screenshot Ref

3. **OSINT Verification Log** with columns:
   - Date/Time | Tool Used | Query Submitted | Result Summary | Screenshot Ref

4. A **Report Draft** document (Word or Markdown) with section headers already in place (see Phase 5 for structure).

### Step 0.3 — Set Your Safety Rules
- **Never click a link.** Only inspect the hyperlink destination by hovering, viewing the HTML source, or copying the raw URL text.
- **Never open or execute an attachment.** Only assess it by filename, extension, and stated type.
- Submit suspicious URLs to OSINT tools (VirusTotal, urlscan.io) rather than visiting them directly — these tools sandbox the check for you.

---

## PHASE 1 — Per-Email Investigation

Repeat this exact checklist for **every single email**, one at a time. Do not skim — treat each one as if it just landed in a real company inbox and your call decides whether it's escalated.

### Step 1.1 — Sender & Header Analysis
For each email, check and record:
- **Display name vs. actual address**: Does "Microsoft Support Team" actually come from a Microsoft domain, or from something like `support@micros0ft-alert.com`?
- **Reply-To field**: Is it different from the From address? A mismatch here is a common redirect tactic used by attackers.
- **Return-Path field** (if visible): Does it point somewhere unrelated to the claimed sender?
- **Domain inspection**:
  - Is it a lookalike/typosquat domain (e.g., `paypa1.com`, `arnazon-support.net`)?
  - Is it a free consumer email provider (Gmail, Outlook.com, Yahoo) being used to send what claims to be official corporate communication?
  - Does the domain use an unusual TLD (.xyz, .top, .info) for a supposedly major brand?
- **Authentication results** (SPF / DKIM / DMARC), if shown in the header data:
  - Note Pass / Fail / None for each.
  - A DMARC/SPF failure on a message claiming to be from a well-known brand is a strong red flag.

### Step 1.2 — Content & Social Engineering Analysis
- Identify which psychological levers are used:
  - **Urgency** ("respond within 24 hours or your account will be locked")
  - **Fear** ("unauthorized login detected")
  - **Authority** ("this is IT Security / your CEO / HR")
  - **Reward/curiosity** ("you've won," "invoice attached," "shared document")
- Note grammar, tone, and formatting inconsistencies — treat this as a *supporting* signal, not standalone proof (attackers increasingly write clean, professional-sounding lures).
- Note any request for credentials, payment, gift cards, or sensitive data — this is a major differentiator between phishing and legitimate mail.

### Step 1.3 — Link Analysis
For every hyperlink present in the email:
- Compare the **displayed anchor text** to the **actual destination URL**. A mismatch (e.g., text says "Sign in to Office365" but the link points to a random domain) is a definitive red flag.
- Check links hidden inside images, logos, or "unsubscribe" footers — these are often overlooked but frequently malicious.
- Record every unique link domain in your IOC list, even if the email overall looks legitimate.

### Step 1.4 — Attachment Analysis
For every attachment (assess by name/type only — do not open):
- **File extension check**: Look for disguised or double extensions (`Invoice_2024.pdf.exe`, `Scan_Doc.zip.scr`).
- **Macro-risk formats**: `.docm`, `.xlsm`, `.pptm` are high-risk when paired with urgency language ("enable macros to view content").
- **Naming pattern**: Generic, vague, or oddly specific names ("Final_Final_Invoice_Urgent.xls") often indicate mass-produced phishing kits.
- Record filename, extension, and stated file type in your IOC list.

### Step 1.5 — Draft the Per-Email Verdict
Write a short paragraph per email in this format:

> "Email #0X is classified as [Risk Level] because [specific evidence: sender mismatch / spoofed domain / malicious link / suspicious attachment / social engineering pattern], as identified in Steps 1.1–1.4."

**Important discipline:** Build the verdict from the evidence you gathered — don't decide the verdict first and then go looking for reasons to justify it.

---

## PHASE 2 — IOC Extraction & Consolidation

### Step 2.1 — Pull Every IOC Into the Master List
Go back through your per-email notes and list every:
- Suspicious sender domain
- Suspicious/malicious URL
- IP address (if visible in headers)
- Suspicious filename or file hash (if computable)

### Step 2.2 — Deduplicate
- If the same domain or URL appears across multiple emails (common in phishing campaigns using the same kit), merge the entries and note all the email numbers where it appeared. This is worth calling out in your report — it signals a coordinated campaign, not isolated incidents.

### Step 2.3 — Document Justification for Each IOC
For every IOC, make sure the "Why Suspicious" column is specific and evidence-based — e.g., "Domain uses homoglyph substitution: 'rn' replacing 'm' in 'arnazon.com'" rather than just "looks suspicious."

---

## PHASE 3 — OSINT Cross-Verification

### Step 3.1 — VirusTotal
- Submit each suspicious domain/URL (paste the URL into VirusTotal's search — do not visit it yourself).
- Record: number of security vendors flagging it, categorization (phishing/malware/malicious), and first-seen date if available.

### Step 3.2 — urlscan.io
- Submit suspicious URLs here to get a sandboxed screenshot and behavior report of what the page actually does.
- Record: verdict, screenshot reference, and any redirect chains observed.

### Step 3.3 — MXToolbox
- Check the sending domain's mail server reputation and blacklist status.
- If accessible, check SPF/DMARC records for the domain being spoofed (useful for showing the *real* organization has proper records that the phishing email fails to match).

### Step 3.4 — Google Safe Browsing (optional additional check)
- Cross-check flagged URLs against Google's Safe Browsing status page for a second opinion.

### Step 3.5 — Log Everything
For every check performed, record in the OSINT Verification Log:
- Date/time of check
- Tool used
- Exact query submitted
- Result summary
- Screenshot (recommended — strengthens your report's credibility)

**Note:** Even for emails that look clearly legitimate, run at least one verification check (e.g., confirm the sender domain's SPF/DMARC record is valid). This demonstrates due diligence rather than assumption — a key evaluation point.

---

## PHASE 4 — Risk Classification

### Step 4.1 — Apply a Consistent Rubric
Use this scale across all emails so classifications are principled, not arbitrary:

| Risk Level | Criteria |
|---|---|
| **Critical** | Confirmed malicious domain/URL (VirusTotal hits) + attachment with executable/macro risk + active credential-harvesting behavior, especially combined with spoofed authority and urgency language |
| **High** | Spoofed/lookalike domain or display-name mismatch + suspicious link, even without a confirmed VirusTotal hit yet, but strong OSINT suspicion |
| **Medium** | Some red flags present (urgency language, minor header anomaly, unverified sender) but no confirmed malicious infrastructure |
| **Low** | Sender domain verified legitimate, headers pass authentication, no malicious indicators found |

### Step 4.2 — Classify Each Email
- Assign one risk level per email.
- Cross-check that your classification matches the evidence documented in Phase 1 and the verification results from Phase 3 — do not classify based on gut feeling alone.

### Step 4.3 — Include the Rubric in Your Report
State this table explicitly in your final report so the evaluator can see *why* each verdict was reached, not just what it was.

---

## PHASE 5 — Report Assembly

### Step 5.1 — Structure the Report
Build the final PDF/document with these sections in order:

1. **Executive Summary**
   - Total emails analyzed, how many were malicious/suspicious/legitimate
   - Key patterns observed (e.g., "3 of 5 phishing emails impersonated the same brand")

2. **Per-Email Findings Table**
   - Columns: Email No. → Verdict → Key Indicators → Risk Level

3. **Detailed Per-Email Write-Ups**
   - The evidence-based paragraphs drafted in Step 1.5, expanded with specifics from Phases 1–3

4. **Consolidated IOC List**
   - Full deduplicated table from Phase 2

5. **OSINT Verification Log**
   - Full table from Phase 3 with tool, query, and result for every check

6. **Recommendations**
   - Technical: enforce DMARC with `p=reject`, tighten SPF/DKIM alignment, sandbox/detonate attachments before delivery, block lookalike domains at the email gateway
   - Process: employee phishing-reporting workflow, periodic simulated phishing tests
   - Awareness: targeted training on urgency-based social engineering, since it was the most common lever observed

### Step 5.2 — Polish and Finalize
- Proofread for consistency between your tables and write-ups (verdicts should match across all sections).
- Convert to PDF as the final submission format.
- Keep the tone professional and factual — write it as if a real security team will act on it.

---

## Suggested Timeline

| Day | Task |
|---|---|
| Day 1 | Phase 0 setup + investigate Emails 1–6 (Phase 1) |
| Day 2 | Investigate Emails 7–12 (Phase 1) + build IOC list (Phase 2) |
| Day 3 | Run all OSINT verifications (Phase 3) + finalize risk classifications (Phase 4) |
| Day 4 | Assemble, write, and polish the final report (Phase 5) |

---

## Self-Check Before Submitting
Ask yourself for each email:
- [ ] Can I explain, in my own words, exactly why this email got its risk level?
- [ ] Is every IOC backed by a clear "why suspicious" explanation?
- [ ] Did I verify at least one thing per email using an OSINT tool, even for legitimate-looking ones?
- [ ] Does my report read like something a real SOC analyst would hand to a security team — evidence-first, not guesswork?
