# Email Threat Investigation Project — UI & Improvement Advice

Consolidated recommendations following a code security review and UI/presentation assessment of the `email-threat-investigation` repository.

---

## PART 1 — UI / Presentation Improvements

The current deliverable is markdown + a JSON blob — functional, but not what a hiring manager or evaluator would call "polished." Since this is meant to look like something a real SOC would hand up the chain, invest effort here:

### 1.1 — Turn the Report Into a Styled HTML/PDF Dashboard, Not Just Markdown
Build a static HTML page (or generate a PDF from one) with:
- **Color-coded risk badges** (red / orange / yellow / green pills next to each email) instead of plain bold text — instantly scannable at a glance.
- **A summary card row at the top**: total emails analyzed, % malicious, % safe, total IOCs extracted, top attack technique observed — the kind of thing an executive skims in 5 seconds without reading the full report.
- **Properly rendered charts**: the existing Mermaid pie chart is currently raw Mermaid syntax sitting in markdown — fine on GitHub, but won't render if opened elsewhere (e.g., pasted into Word, viewed in a plain text editor, or converted to PDF naively). Render it as an actual image/SVG or embed a JS charting library.
- **Collapsible per-email cards** instead of one long scroll — makes 13 emails feel navigable, not exhausting to read through.

### 1.2 — Add a Timeline View
All 13 emails span July 3–13, 2026. A horizontal timeline (Mermaid Gantt chart or a simple chart) showing when each email landed, color-coded by risk level, tells a much better "story" than a table alone. It visually surfaces the attack campaign accelerating (multiple BEC/phishing attempts clustering mid-July) — exactly the kind of pattern-recognition insight a real SOC report should highlight, not bury in a table.

### 1.3 — Make the IOC Table Filterable/Searchable
If the report is HTML, a plain table with a small JavaScript search box (even a 10-line vanilla JS filter function) turns the IOC list from "read the whole thing" into "type 'docm' and find it instantly." Small effort, disproportionate polish payoff.

### 1.4 — Add an "At a Glance" Triage Board
Build a Kanban-style view — Safe / Medium / Critical columns with each email as a card in the relevant column — rather than relying only on a table. This communicates severity distribution faster visually than any table format and mirrors how real SOC ticketing/triage tools present a queue.

---

## PART 2 — Code & Tooling Improvements

(These build on the critical/high findings from the security review — see Part 4 below for those specifics.)

### 2.1 — Documentation
- Add a **`README.md`** with setup and run instructions. Right now someone has to guess how `soc_email_parser.py` and `generate_sample_emails.py` relate to each other and in what order to run them.
- Add a **`requirements.txt`** — even though the parser currently only needs the Python standard library, state this explicitly so graders/evaluators don't wonder if a dependency is missing.

### 2.2 — Better CLI Behavior
- Add a `--verbose` / `-v` flag and basic logging instead of bare `print()` statements. Looks more like production tooling and gives control over output noise.
- Add a config file (e.g., `known_good_domains.json`) listing the organization's legitimate domains (`solvexindustries.com`, `tallysolutions.com`, etc.) so the parser can auto-flag `From` domains that **don't** match as "external/unverified." This converts a chunk of manual analyst judgment into automation — which is the actual point of building a SOC tool rather than just a data extractor.

### 2.3 — Export Formats That Matter for Real Workflows
- Add a `--export-stix` or `--export-csv` option for the IOC list. Real SOC teams feed IOCs into SIEM/firewall blocklists, and STIX 2.1 or a simple CSV (`indicator,type,description`) is the actual format consumed downstream — this demonstrates understanding of where the tool's output goes operationally, not just that it produces *a* JSON file.

### 2.4 — Testing
- Add a small `tests/` folder with 2–3 `pytest` cases, for example:
  - An attachment declared with `Content-Disposition: inline` is still detected (regression test for the Critical bypass found in review).
  - SHA-256 output matches a known value for a fixed test payload.
  - Old-style `Content-Type: name=` attachments (no `Content-Disposition` header) are still detected.
- This both proves the Critical bugs from the security review are fixed and demonstrates testing discipline in the submission — evaluators notice this.

### 2.5 — Pipeline Automation
- Add a single `run_investigation.sh` (or a `Makefile` target) that runs: generate emails → parse them → build the HTML dashboard → output the final PDF, all in one command. Turns "here are some scripts" into "here's a pipeline" — reads much more like a real internal tool than a collection of standalone files.

---

## PART 3 — Report Content Gaps (Recap From Earlier Review)

These are separate from UI/code — they affect the actual investigative deliverable and should be closed before final submission:

1. **Missing OSINT Verification Log.** The assignment explicitly requires documented VirusTotal/urlscan.io/MXToolbox checks with tool name, query, and result. Currently absent entirely from both report files. Even for synthetic/instructional domains, document the null result and explain why classification still stands on header/content evidence.
2. **IOC table mislabeling.** `s.iyer.cfo.travel@outlook.com` is listed as a "Domain" IOC — it's an email address (Reply-To hijack indicator). Split into a separate "Email Address" IOC type; don't list `outlook.com` itself as malicious infrastructure.
3. **Computed SHA-256 hashes aren't surfaced in the report**, even though the parser computes them. Hashes are a higher-fidelity IOC than filenames (which attackers can trivially rename) — pull them into the Master IOC table.
4. **Domain naming inconsistency**: report cites `micros0ft-online.com`; parser extracted the more specific `login.micros0ft-online.com` from the actual phishing link. Reconcile on the more precise, actionable subdomain for blocking purposes.

---

## PART 4 — Security Findings Recap (Code-Level, From Hands-On Testing)

For reference — these were confirmed by actually running the parser against crafted test files, not just reading the code:

| Severity | Finding | Fix |
|---|---|---|
| **Critical** | Attachments with `Content-Disposition: inline` are completely invisible — confirmed by test (flipped a `.docm` attachment's disposition header; parser found zero attachments, zero hash, zero flag). | Trigger attachment processing on `part.get_filename()` being truthy, not on the `"attachment"` substring in Content-Disposition. |
| **Critical** | Old-style attachments declared only via `Content-Type: name=` (no `Content-Disposition` header) are also invisible — confirmed by test. | Same fix as above — filename presence should be the trigger, regardless of how it was declared. |
| **High** | `Received` header (and therefore all IP evidence) is never extracted by the parser — root cause of the mismatch between the narrative report's IPs (accurate, manually transcribed) and `parsed_iocs.json` (zero IPs everywhere). | Add `Received` to the extracted headers dict and run `REGEX_IP` against it specifically. |
| **High** | No IDN/homograph decoding on extracted domains — a punycode homograph domain would show as raw `xn--...` with no flag or decoded comparison. | Add `idna` decode step and flag domains that decode to something visually similar to known brands. |
| **Medium** | Private-IP filtering only checks `127.`, `10.`, `192.168.` — misses the rest of RFC1918 (`172.16–172.31`) and link-local (`169.254`). | Replace prefix-string checks with `ipaddress.ip_address(ip).is_private`. |
| **Medium** | Extension-spoofing detection doesn't catch RTLO Unicode tricks (e.g., reversed filename extensions) — a known email attachment spoofing technique. | Add a check for `\u202e` (RTLO) and similar Unicode control characters in filenames. |
| **Medium** | `REGEX_DOMAIN` is defined but never used anywhere in the code (dead code). | Either use it to catch bare domains mentioned in body text without a scheme, or remove it. |
| **Low** | Hardcoded Windows absolute path (`c:\Email\sample_emails`) in `generate_sample_emails.py` — won't run for anyone else without manual edits. | Use a relative path or `argparse` output directory argument. |
| **Good practice confirmed** | No secrets found anywhere in the repo or git history (single clean commit). | — |
| **Good practice confirmed** | No live malicious code shipped — attachments are inert placeholder bytes, not real macro payloads. | — |

---

## Suggested Priority Order

1. Fix the two Critical attachment-detection bypasses (Part 4) — these undermine the tool's core function.
2. Add the OSINT Verification Log (Part 3, item 1) — required deliverable currently missing.
3. Build the HTML dashboard (Part 1) — highest-visible-impact polish item.
4. Add README + requirements.txt (Part 2.1) — quick wins, immediately improves professionalism.
5. Everything else (tests, exports, automation pipeline) as time allows — these strengthen the submission but aren't blocking issues.
