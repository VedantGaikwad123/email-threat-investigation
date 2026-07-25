#!/usr/bin/env python3
"""
Sample EML Generator for Case File CA-ETI-01 (Solvex Industries Pvt. Ltd.)
Extracted from c:\\Email\\emails.pdf (13 Emails total)
"""

import os
from email.message import EmailMessage

SAMPLE_DIR = "c:\\Email\\sample_emails"

EMAILS_DATA = [
    {
        "filename": "Email_01.eml",
        "from": "IT Helpdesk – Solvex Industries <ithelpdesk@solvexindustries.com>",
        "reply_to": "ithelpdesk@solvexindustries.com",
        "return_path": "ithelpdesk@solvexindustries.com",
        "to": "aditya.rao@solvexindustries.com",
        "subject": "Password Expiry Reminder – Action Needed Within 5 Days",
        "date": "03 July 2026, 10:12 AM IST",
        "auth": "spf=pass; dkim=pass; dmarc=pass (TLS 1.3)",
        "body": "Dear Aditya,\n\nThis is an automated reminder from the IT Helpdesk. Our records show that your network account password is due to expire in 5 days, as per the company's 90-day password rotation policy.\n\nTo avoid any interruption to your email or system access, please update your password before the expiry date. You can do this at any time by logging into the internal IT Service Portal from your office desktop or the VPN-connected laptop and navigating to Account Settings > Change Password.\n\nIf you face any difficulty resetting your password, please raise a ticket through the IT Service Portal or contact the Helpdesk extension 204 during working hours. Do not share your password with anyone, including IT staff, over email, call or chat.\n\nRegards,\nIT Helpdesk Team\nSolvex Industries Pvt. Ltd."
    },
    {
        "filename": "Email_02.eml",
        "from": "IT Support Desk <support@solvex-industries-helpdesk.com>",
        "reply_to": "recovery-team@mail-secure-verify.net",
        "return_path": "bounce@mail-secure-verify.net",
        "to": "aditya.rao@solvexindustries.com",
        "bcc": "allstaff-list223@solvex-industries-helpdesk.com",
        "subject": "URGENT: Your Mailbox Storage is FULL – Verify Now to Avoid Suspension",
        "date": "05 July 2026, 11:47 PM IST",
        "auth": "spf=fail; dkim=fail; dmarc=fail (Reject policy overridden)",
        "body": "Dear User,\n\nYour mailbox has exceeded its allocated storage limit of 5GB. As per policy, mailboxes exceeding this limit for more than 24 hours will be automatically suspended and all incoming mail will be permanently rejected.\n\nTo avoid suspension of your account, you are required to verify your identity IMMEDIATELY by clicking the secure link below and confirming your login credentials. This process takes less than 2 minutes.\n\nLink: http://solvex-industries-helpdesk.verify-account-secure.com/mailbox/confirm?user=aditya.rao\n\nFailure to verify within 24 hours will result in permanent loss of access to your mailbox and all stored data. This is a final notice.\n\nThank you for your prompt action.\nIT Support Team"
    },
    {
        "filename": "Email_03.eml",
        "from": "Ramesh Kulkarni – Accounts, Apex Steel Traders <ramesh.kulkarni@apex-steeltraders.co>",
        "reply_to": "accounts.payments@apexsteel-billing.com",
        "return_path": "ramesh.kulkarni@apex-steeltraders.co",
        "to": "aditya.rao@solvexindustries.com",
        "cc": "priya.menon@solvexindustries.com",
        "subject": "Invoice SI-4471 & Updated Bank Details for Future Payments",
        "date": "07 July 2026, 3:28 PM IST",
        "auth": "spf=pass (for apex-steeltraders.co); dkim=pass; dmarc=pass (TLS 1.2)",
        "body": "Dear Aditya,\n\nPlease find attached Invoice SI-4471 for the steel coil consignment supplied to your Nagpur unit last month, amounting to Rs. 4,85,600/-.\n\nAs part of our internal banking audit, our current account has been temporarily restricted. Kindly note that all payments from this point forward should be made to our NEW account, details of which are mentioned in the attached invoice, and NOT our previously shared account. This change is effective immediately.\n\nWe would appreciate it if this payment could be processed on priority, as our finance team needs to close this quarter's books by the 10th. Please confirm once the transfer has been initiated so we can update our records.\n\nRegards,\nRamesh Kulkarni\nAccounts Department, Apex Steel Traders",
        "attachment": ("Invoice_SI-4471_Apex_Steel.pdf", b"MOCK_PDF_PAYMENT_REDIRECTION_INVOICE")
    },
    {
        "filename": "Email_04.eml",
        "from": "Human Resources – Solvex Industries <hr@solvexindustries.com>",
        "reply_to": "hr@solvexindustries.com",
        "return_path": "hr@solvexindustries.com",
        "to": "all-employees@solvexindustries.com",
        "subject": "Revised Leave & Work-From-Home Policy – Effective 15 July 2026",
        "date": "08 July 2026, 9:05 AM IST",
        "auth": "spf=pass; dkim=pass; dmarc=pass (TLS 1.3)",
        "body": "Dear Team,\n\nAs communicated in last month's town hall, the revised Leave and Work-From-Home Policy will come into effect from 15th July 2026. Key changes include an increase in casual leave from 8 to 10 days per year, and a structured hybrid work option of up to 2 WFH days per week subject to manager approval.\n\nThe complete policy document has been uploaded to the HR Portal under Policies > Leave Policy 2026. Please log in using your employee credentials to review the full document.\n\nIf you have questions regarding the revised policy, please reach out to your respective HR Business Partner or attend the Q&A session scheduled for 12th July at 4:00 PM in Conference Room 2.\n\nWarm regards,\nHuman Resources Team\nSolvex Industries Pvt. Ltd."
    },
    {
        "filename": "Email_05.eml",
        "from": "Rajeev Malhotra (Managing Director) <rajeev.malhotra.md@gmail-corpmail.com>",
        "reply_to": "rajeev.malhotra.md@gmail-corpmail.com",
        "return_path": "rajeev.malhotra.md@gmail-corpmail.com",
        "to": "aditya.rao@solvexindustries.com",
        "subject": "Confidential – Immediate Wire Transfer Required (Time Sensitive)",
        "date": "09 July 2026, 1:14 PM IST",
        "auth": "spf=none; dkim=none; dmarc=none",
        "body": "Aditya,\n\nI'm currently in a board meeting with our overseas investors and cannot take calls right now. I need you to process an urgent international wire transfer of USD 18,500 to close a confidential acquisition deal today. This is extremely time sensitive and must be kept strictly between us until I announce it to the board.\n\nI will send the beneficiary bank details in my next email. Please confirm you can initiate this within the next hour and let me know once done. Do not discuss this with Priya or anyone in Accounts for now — I want to keep this quiet until the deal is signed.\n\nI'm counting on you for this one. Talk soon.\n\nRajeev"
    },
    {
        "filename": "Email_06.eml",
        "from": "Google Drive <drive-shares-noreply@google.com>",
        "reply_to": "drive-shares-noreply@google.com",
        "return_path": "drive-shares-noreply@google.com",
        "to": "aditya.rao@solvexindustries.com",
        "subject": "'Q1_Vendor_Compliance_Report.xlsx' has been shared with you",
        "date": "09 July 2026, 6:40 PM IST",
        "auth": "spf=pass; dkim=pass; dmarc=pass (TLS 1.3)",
        "body": "priya.menon@solvexindustries.com shared a file with you:\nQ1_Vendor_Compliance_Report.xlsx\n\nPriya added a note: \"Hi Aditya, sharing the vendor compliance sheet we discussed in today's finance sync. Can you review the highlighted rows before Friday's audit call? Thanks!\"\n\nOpen in Google Sheets: https://docs.google.com/spreadsheets/d/1kQ3z-example-fileid-9f2/edit?usp=sharing"
    },
    {
        "filename": "Email_07.eml",
        "from": "Microsoft account team <security-noreply@micros0ft-online.com>",
        "reply_to": "no-reply@micros0ft-online.com",
        "return_path": "bounce@micros0ft-online.com",
        "to": "aditya.rao@solvexindustries.com",
        "subject": "Unusual sign-in activity detected on your Microsoft account",
        "date": "10 July 2026, 2:03 AM IST",
        "auth": "spf=fail; dkim=fail; dmarc=fail",
        "body": "Microsoft account\n\nWe detected an unusual sign-in attempt on your account from a new device in Lagos, Nigeria on 10 July 2026 at 1:58 AM. If this wasn't you, your account may be compromised.\n\nFor your security, we have temporarily limited access to your account. To restore full access, please verify your identity within 12 hours by confirming your account details using the secure link below:\n\nhttp://login.micros0ft-online.com/secure/verify-identity?ref=aditya.rao\n\nIf you don't recognise this activity, we strongly recommend you review your account immediately to prevent unauthorized access to your email, OneDrive files and Teams messages.\n\nThanks,\nThe Microsoft account team"
    },
    {
        "filename": "Email_08.eml",
        "from": "Neha Kapoor, HR Consultant <neha.kapoor.hr@talentbridge-recruiters.net>",
        "reply_to": "neha.kapoor.hr@talentbridge-recruiters.net",
        "return_path": "neha.kapoor.hr@talentbridge-recruiters.net",
        "to": "aditya.rao@solvexindustries.com",
        "subject": "Exciting Career Opportunity – Senior Finance Role (Immediate Response Needed)",
        "date": "10 July 2026, 11:20 AM IST",
        "auth": "spf=pass (for talentbridge-recruiters.net); dkim=pass; dmarc=none",
        "body": "Dear Candidate,\n\nYour profile has been shortlisted for a Senior Finance Manager position with a leading MNC client of ours, offering a salary 40% higher than industry average. We are impressed by your experience and would like to move forward quickly as the client wants to close this position this week.\n\nAttached is the detailed Job Description along with the client company profile and compensation structure for your review. Please go through it and reply within 24 hours confirming your interest, along with a scanned copy of your latest salary slip and PAN card for our internal verification process.\n\nLooking forward to your quick response so we can schedule your interview at the earliest.\n\nBest regards,\nNeha Kapoor\nSenior HR Consultant, TalentBridge Recruiters",
        "attachment": ("JD_SeniorFinanceManager_Client.zip", b"MOCK_ZIP_JOB_DESCRIPTION_ATTACHMENT")
    },
    {
        "filename": "Email_09.eml",
        "from": "Tally Solutions Billing <billing@tallysolutions.com>",
        "reply_to": "billing@tallysolutions.com",
        "return_path": "billing@tallysolutions.com",
        "to": "aditya.rao@solvexindustries.com",
        "cc": "accounts@solvexindustries.com",
        "subject": "Your TallyPrime Cloud Subscription Renewal Invoice – INV-88213",
        "date": "11 July 2026, 10:00 AM IST",
        "auth": "spf=pass; dkim=pass; dmarc=pass (TLS 1.3)",
        "body": "Dear Customer,\n\nThis is to notify you that your TallyPrime Cloud annual subscription (License ID: TP-2291-SOLVEX) is due for renewal on 20 July 2026. The renewal invoice INV-88213 for Rs. 32,500/- (inclusive of GST) is attached for your records.\n\nPayments can be made through your existing registered payment method on the Tally Customer Portal, or via NEFT/RTGS to the bank account already on file with our billing team — no bank details have changed.\n\nIf you wish to modify your plan or add additional user licenses before renewal, please contact your Tally partner or our billing support at billing@tallysolutions.com.\n\nThank you for being a valued customer.\n\nTally Solutions Pvt. Ltd. – Billing Team",
        "attachment": ("INV-88213_TallyPrime_Renewal.pdf", b"MOCK_PDF_TALLY_SUBSCRIPTION_INVOICE")
    },
    {
        "filename": "Email_10.eml",
        "from": "INTERNATIONAL LOTTERY BOARD <claims.department009@yandex-mailer.com>",
        "reply_to": "agent.williams.claims@outlook-verify.info",
        "return_path": "claims.department009@yandex-mailer.com",
        "to": "undisclosed-recipients",
        "bcc": "aditya.rao@solvexindustries.com",
        "subject": "CONGRATULATIONS!!! YOU HAVE WON USD 1,000,000 IN THE INTERNATIONAL EMAIL LOTTERY",
        "date": "11 July 2026, 4:52 PM IST",
        "auth": "spf=fail; dkim=fail; dmarc=fail",
        "body": "ATTENTION WINNER,\n\nWe are pleased to inform you that your email address has WON the sum of USD 1,000,000.00 (One Million US Dollars Only) in the International Email Lottery Programme 2026, held under the supervision of the European Lottery Commission.\n\nTo claim your prize, you are required to contact our Claims Agent immediately with your full name, address, phone number, and a copy of your ID for verification. A small processing and courier fee of USD 250 will be required to release your winning certificate and cheque.\n\nLink: http://claim-your-prize-now.lottery-verify.info/claim?ref=44921\n\nPlease respond within 48 hours failure of which your prize will be forfeited and awarded to another participant.\n\nCongratulations once again!\nDr. James Williams, Claims Coordinator"
    },
    {
        "filename": "Email_11.eml",
        "from": "Suresh Iyer (CFO) <suresh.iyer@solvexindustries.com>",
        "reply_to": "s.iyer.cfo.travel@outlook.com",
        "return_path": "suresh.iyer@solvexindustries.com",
        "to": "aditya.rao@solvexindustries.com",
        "subject": "Quick request before my flight",
        "date": "12 July 2026, 8:31 AM IST",
        "auth": "spf=pass (envelope sender matches solvexindustries.com); dkim=pass; dmarc=pass (TLS 1.3)",
        "body": "Aditya,\n\nAbout to board my flight to Mumbai and my corporate card isn't working at the airport lounge. Can you do me a favour and buy 5 Amazon gift cards of Rs. 5,000 each from the online store, then send me the card codes here — I'll reimburse you as soon as I land. Need it in the next 20 minutes before boarding closes.\n\nPlease don't call the office landline about this, my phone network is patchy while boarding, email is easier to check. Really appreciate this, will make it up to you.\n\nSuresh"
    },
    {
        "filename": "Email_12.eml",
        "from": "Information Security Team – Solvex Industries <infosec@solvexindustries.com>",
        "reply_to": "infosec@solvexindustries.com",
        "return_path": "infosec@solvexindustries.com",
        "to": "all-employees@solvexindustries.com",
        "subject": "Reminder: Mandatory Security Awareness Training – Due This Friday",
        "date": "12 July 2026, 9:15 AM IST",
        "auth": "spf=pass; dkim=pass; dmarc=pass (TLS 1.3)",
        "body": "Dear Colleague,\n\nThis is a reminder that the mandatory Q3 Security Awareness Training module, covering phishing identification, password hygiene and safe attachment handling, must be completed on the internal Learning Portal by this Friday, 17 July 2026.\n\nAs highlighted in recent incidents across the industry, email-based fraud continues to be one of the top risks to organisations. This training will take approximately 25 minutes to complete and includes a short assessment at the end.\n\nTo access the module, log in to learn.solvexindustries.com using your employee ID. If you experience any login issues, please raise a request with the IT Helpdesk through the official portal.\n\nRegards,\nInformation Security Team\nSolvex Industries Pvt. Ltd."
    },
    {
        "filename": "Email_13.eml",
        "from": "Accounts Receivable <accounts.receivable@shreeganesh-logistics.in>",
        "reply_to": "accounts.receivable@shreeganesh-logistics.in",
        "return_path": "mailer@shreeganesh-logistics.in",
        "to": "aditya.rao@solvexindustries.com",
        "subject": "Pending Invoice – Please Review & Process on Priority",
        "date": "13 July 2026, 5:58 PM IST",
        "auth": "spf=fail (domain not authorised to send); dkim=none; dmarc=fail",
        "body": "Dear Sir,\n\nPlease find attached the pending transport invoice for the last three consignments dispatched to your Pune warehouse. Kindly review and process the payment at the earliest as our accounts are overdue for closing this month.\n\nThe attached file also contains the delivery challans and updated GST details for your reference. Please enable editing/macros if prompted so all the invoice tables display correctly, as the file was generated on an older billing system.\n\nLink: http://shreeganesh-logistics.in.invoice-view-secure.com/download?file=inv2207\n\nKindly confirm receipt of this email and expected date of payment.\n\nThanking you,\nAccounts Receivable Team\nShree Ganesh Logistics",
        "attachment": ("Pending_Invoice_Challan_Details.docm", b"MOCK_DOCM_VBA_MACRO_PAYLOAD")
    }
]

def main():
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    print(f"[*] Generating 13 sample .eml files from Case File CA-ETI-01 into {SAMPLE_DIR}...")
    
    for item in EMAILS_DATA:
        msg = EmailMessage()
        msg['From'] = item['from']
        if item.get('reply_to'):
            msg['Reply-To'] = item['reply_to']
        if item.get('return_path'):
            msg['Return-Path'] = item['return_path']
        msg['To'] = item['to']
        if item.get('cc'):
            msg['Cc'] = item['cc']
        if item.get('bcc'):
            msg['Bcc'] = item['bcc']
        msg['Subject'] = item['subject']
        msg['Date'] = item['date']
        msg['Authentication-Results'] = item['auth']
        msg.set_content(item['body'])
        
        if 'attachment' in item:
            fname, fdata = item['attachment']
            msg.add_attachment(fdata, maintype='application', subtype='octet-stream', filename=fname)

        file_path = os.path.join(SAMPLE_DIR, item['filename'])
        with open(file_path, 'wb') as f:
            f.write(msg.as_bytes())
        print(f" [+] Generated {item['filename']}")

    print("\n[*] All 13 sample .eml artifacts generated successfully.")

if __name__ == "__main__":
    main()
