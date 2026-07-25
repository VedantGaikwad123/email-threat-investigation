#!/usr/bin/env python3
"""
Sample EML Generator for SOC Email Threat Simulation
Case File CA-ETI-01 — Solvex Industries Pvt. Ltd.
Creates 13 sample .eml files representing diverse threat categories.
"""

import os
import argparse
from email.message import EmailMessage

EMAILS_DATA = [
    {
        "filename": "Email_01.eml",
        "from": "IT Helpdesk - Solvex Industries <ithelpdesk@solvexindustries.com>",
        "reply_to": "ithelpdesk@solvexindustries.com",
        "to": "aditya.rao@solvexindustries.com",
        "subject": "Password Expiry Reminder - Action Needed Within 5 Days",
        "date": "03 Jul 2026 10:12:00 +0530",
        "auth": "spf=pass; dkim=pass; dmarc=pass (TLS 1.3)",
        "received": "from mail.solvexindustries.com (192.168.14.22) by mx.solvexindustries.com",
        "body": "Dear Aditya,\n\nThis is an automated reminder from the IT Helpdesk. Your network account password is due to expire in 5 days as per the company's 90-day password rotation policy.\n\nTo avoid interruption, please update your password by logging into the internal IT Service Portal. Do not share your password with anyone, including IT staff.\n\nRegards,\nIT Helpdesk Team\nSolvex Industries Pvt. Ltd."
    },
    {
        "filename": "Email_02.eml",
        "from": "IT Support Desk <support@solvex-industries-helpdesk.com>",
        "reply_to": "recovery-team@mail-secure-verify.net",
        "to": "aditya.rao@solvexindustries.com",
        "subject": "URGENT: Your Mailbox Storage is FULL - Verify Now to Avoid Suspension",
        "date": "05 Jul 2026 23:47:00 +0530",
        "auth": "spf=fail; dkim=fail; dmarc=fail (Reject policy overridden)",
        "received": "from unknown-host-193.41.77.108.static-cloud.ru (193.41.77.108)",
        "body": "Dear User,\n\nYour mailbox has exceeded its allocated 5GB limit. Mailboxes exceeding this limit for more than 24 hours will be automatically suspended.\n\nVerify your identity IMMEDIATELY: http://solvex-industries-helpdesk.verify-account-secure.com/mailbox/confirm?user=aditya.rao\n\nFailure to verify within 24 hours will result in permanent loss of access.\n\nIT Support Team"
    },
    {
        "filename": "Email_03.eml",
        "from": "Ramesh Kulkarni - Accounts <ramesh.kulkarni@apex-steeltraders.co>",
        "reply_to": "accounts.payments@apexsteel-billing.com",
        "to": "aditya.rao@solvexindustries.com",
        "cc": "priya.menon@solvexindustries.com",
        "subject": "Invoice SI-4471 & Updated Bank Details for Future Payments",
        "date": "07 Jul 2026 15:28:00 +0530",
        "auth": "spf=pass (for apex-steeltraders.co); dkim=pass; dmarc=pass (TLS 1.2)",
        "received": "from mail.apex-steeltraders.co (103.22.8.190)",
        "body": "Dear Aditya,\n\nPlease find attached Invoice SI-4471 for Rs. 4,85,600/-.\n\nDue to an internal banking audit, our current account has been temporarily restricted. Kindly make all future payments to our NEW account as mentioned in the attached invoice. Please process on priority before the 10th.\n\nRegards,\nRamesh Kulkarni\nAccounts Department, Apex Steel Traders",
        "attachment": ("Invoice_SI-4471_Apex_Steel.pdf", b"MOCK_PDF_PAYMENT_REDIRECTION_INVOICE")
    },
    {
        "filename": "Email_04.eml",
        "from": "Human Resources - Solvex Industries <hr@solvexindustries.com>",
        "reply_to": "hr@solvexindustries.com",
        "to": "all-employees@solvexindustries.com",
        "subject": "Revised Leave & Work-From-Home Policy - Effective 15 July 2026",
        "date": "08 Jul 2026 09:05:00 +0530",
        "auth": "spf=pass; dkim=pass; dmarc=pass (TLS 1.3)",
        "received": "from mail.solvexindustries.com (192.168.14.19)",
        "body": "Dear Team,\n\nThe revised Leave and Work-From-Home Policy will come into effect from 15th July 2026. Key changes include an increase in casual leave from 8 to 10 days per year, and a hybrid work option of up to 2 WFH days per week subject to manager approval.\n\nThe complete policy document has been uploaded to the HR Portal under Policies > Leave Policy 2026.\n\nHuman Resources Team\nSolvex Industries Pvt. Ltd."
    },
    {
        "filename": "Email_05.eml",
        "from": "Rajeev Malhotra (Managing Director) <rajeev.malhotra.md@gmail-corpmail.com>",
        "reply_to": "rajeev.malhotra.md@gmail-corpmail.com",
        "to": "aditya.rao@solvexindustries.com",
        "subject": "Confidential - Immediate Wire Transfer Required (Time Sensitive)",
        "date": "09 Jul 2026 13:14:00 +0530",
        "auth": "spf=none; dkim=none; dmarc=none",
        "received": "from smtp-relay-88.freemailhost.io (45.137.22.9)",
        "body": "Aditya,\n\nI'm currently in a board meeting and cannot take calls. I need you to process an urgent international wire transfer of USD 18,500 to close a confidential acquisition deal today. Keep this strictly between us until I announce it.\n\nI will send beneficiary bank details in my next email. Please confirm you can initiate this within the next hour.\n\nRajeev"
    },
    {
        "filename": "Email_06.eml",
        "from": "Google Drive <drive-shares-noreply@google.com>",
        "reply_to": "drive-shares-noreply@google.com",
        "to": "aditya.rao@solvexindustries.com",
        "subject": "'Q1_Vendor_Compliance_Report.xlsx' has been shared with you",
        "date": "09 Jul 2026 18:40:00 +0530",
        "auth": "spf=pass; dkim=pass; dmarc=pass (TLS 1.3)",
        "received": "from mail-sor-f89.google.com (209.85.220.89)",
        "body": "priya.menon@solvexindustries.com shared a file with you:\nQ1_Vendor_Compliance_Report.xlsx\n\nNote: Hi Aditya, sharing the vendor compliance sheet from today's finance sync. Can you review the highlighted rows before Friday's audit call?\n\nOpen in Sheets: https://docs.google.com/spreadsheets/d/1kQ3z-example-fileid-9f2/edit?usp=sharing"
    },
    {
        "filename": "Email_07.eml",
        "from": "Microsoft account team <security-noreply@micros0ft-online.com>",
        "reply_to": "no-reply@micros0ft-online.com",
        "to": "aditya.rao@solvexindustries.com",
        "subject": "Unusual sign-in activity detected on your Microsoft account",
        "date": "10 Jul 2026 02:03:00 +0530",
        "auth": "spf=fail; dkim=fail; dmarc=fail",
        "received": "from host-77-91-134-6.vpn-exit.net (77.91.134.6)",
        "body": "Microsoft account\n\nWe detected an unusual sign-in attempt from Lagos, Nigeria on 10 July at 1:58 AM. Your account may be compromised.\n\nVerify your identity within 12 hours: http://login.micros0ft-online.com/secure/verify-identity?ref=aditya.rao\n\nIf you do not recognise this, review your account immediately.\n\nThe Microsoft account team"
    },
    {
        "filename": "Email_08.eml",
        "from": "Neha Kapoor, HR Consultant <neha.kapoor.hr@talentbridge-recruiters.net>",
        "reply_to": "neha.kapoor.hr@talentbridge-recruiters.net",
        "to": "aditya.rao@solvexindustries.com",
        "subject": "Exciting Career Opportunity - Senior Finance Role (Immediate Response Needed)",
        "date": "10 Jul 2026 11:20:00 +0530",
        "auth": "spf=pass (for talentbridge-recruiters.net); dkim=pass; dmarc=none",
        "received": "from mail.talentbridge-recruiters.net (156.213.44.71)",
        "body": "Dear Candidate,\n\nYour profile has been shortlisted for a Senior Finance Manager role offering a salary 40% above industry average. We would like to move forward quickly.\n\nPlease review the attached Job Description and reply within 24 hours with your interest, along with a scanned copy of your latest salary slip and PAN card for our internal verification.\n\nBest regards,\nNeha Kapoor\nSenior HR Consultant, TalentBridge Recruiters",
        "attachment": ("JD_SeniorFinanceManager_Client.zip", b"MOCK_ZIP_JOB_DESCRIPTION_ATTACHMENT")
    },
    {
        "filename": "Email_09.eml",
        "from": "Tally Solutions Billing <billing@tallysolutions.com>",
        "reply_to": "billing@tallysolutions.com",
        "to": "aditya.rao@solvexindustries.com",
        "cc": "accounts@solvexindustries.com",
        "subject": "Your TallyPrime Cloud Subscription Renewal Invoice - INV-88213",
        "date": "11 Jul 2026 10:00:00 +0530",
        "auth": "spf=pass; dkim=pass; dmarc=pass (TLS 1.3)",
        "received": "from mta-out.tallysolutions.com (203.0.113.44)",
        "body": "Dear Customer,\n\nYour TallyPrime Cloud annual subscription (License ID: TP-2291-SOLVEX) is due for renewal on 20 July 2026. Invoice INV-88213 for Rs. 32,500/- (inclusive of GST) is attached.\n\nPayments can be made through your registered payment method. No bank details have changed.\n\nThank you for being a valued customer.\n\nTally Solutions Pvt. Ltd.",
        "attachment": ("INV-88213_TallyPrime_Renewal.pdf", b"MOCK_PDF_TALLY_SUBSCRIPTION_INVOICE")
    },
    {
        "filename": "Email_10.eml",
        "from": "INTERNATIONAL LOTTERY BOARD <claims.department009@yandex-mailer.com>",
        "reply_to": "agent.williams.claims@outlook-verify.info",
        "to": "undisclosed-recipients@solvexindustries.com",
        "subject": "CONGRATULATIONS!!! YOU HAVE WON USD 1,000,000 IN THE INTERNATIONAL EMAIL LOTTERY",
        "date": "11 Jul 2026 16:52:00 +0530",
        "auth": "spf=fail; dkim=fail; dmarc=fail",
        "received": "from unknown-relay-node4.freehosting-mail.com (185.220.101.44)",
        "body": "ATTENTION WINNER,\n\nYour email address has WON USD 1,000,000.00 in the International Email Lottery Programme 2026. To claim your prize, contact our Claims Agent with your full name, address, phone number, and ID.\n\nA processing and courier fee of USD 250 is required to release your winning certificate.\n\nClaim here: http://claim-your-prize-now.lottery-verify.info/claim?ref=44921\n\nRespond within 48 hours.\n\nDr. James Williams, Claims Coordinator"
    },
    {
        "filename": "Email_11.eml",
        "from": "Suresh Iyer (CFO) <suresh.iyer@solvexindustries.com>",
        "reply_to": "s.iyer.cfo.travel@outlook.com",
        "to": "aditya.rao@solvexindustries.com",
        "subject": "Quick request before my flight",
        "date": "12 Jul 2026 08:31:00 +0530",
        "auth": "spf=pass (envelope sender matches solvexindustries.com); dkim=pass; dmarc=pass (TLS 1.3)",
        "received": "from mail.solvexindustries.com (192.168.14.19)",
        "body": "Aditya,\n\nAbout to board my flight and my corporate card isn't working. Can you buy 5 Amazon gift cards of Rs. 5,000 each and send me the card codes? I'll reimburse you as soon as I land. Need it in the next 20 minutes.\n\nPlease don't call the office landline — email is easier while boarding.\n\nSuresh"
    },
    {
        "filename": "Email_12.eml",
        "from": "Information Security Team - Solvex Industries <infosec@solvexindustries.com>",
        "reply_to": "infosec@solvexindustries.com",
        "to": "all-employees@solvexindustries.com",
        "subject": "Reminder: Mandatory Security Awareness Training - Due This Friday",
        "date": "12 Jul 2026 09:15:00 +0530",
        "auth": "spf=pass; dkim=pass; dmarc=pass (TLS 1.3)",
        "received": "from mail.solvexindustries.com (192.168.14.19)",
        "body": "Dear Colleague,\n\nThe mandatory Q3 Security Awareness Training module must be completed on the internal Learning Portal by this Friday, 17 July 2026. The training takes approximately 25 minutes.\n\nLog in to learn.solvexindustries.com using your employee ID.\n\nInformation Security Team\nSolvex Industries Pvt. Ltd."
    },
    {
        "filename": "Email_13.eml",
        "from": "Accounts Receivable <accounts.receivable@shreeganesh-logistics.in>",
        "reply_to": "accounts.receivable@shreeganesh-logistics.in",
        "to": "aditya.rao@solvexindustries.com",
        "subject": "Pending Invoice - Please Review & Process on Priority",
        "date": "13 Jul 2026 17:58:00 +0530",
        "auth": "spf=fail (domain not authorised to send); dkim=none; dmarc=fail",
        "received": "from webmail-host-4.sharedhosting-cluster.com (41.203.88.17)",
        "body": "Dear Sir,\n\nPlease find attached the pending transport invoice for the last three consignments to your Pune warehouse. Kindly process the payment at the earliest.\n\nPlease enable editing/macros if prompted so all invoice tables display correctly, as the file was generated on an older billing system.\n\nDownload here: http://shreeganesh-logistics.in.invoice-view-secure.com/download?file=inv2207\n\nThank you,\nAccounts Receivable Team\nShree Ganesh Logistics",
        "attachment": ("Pending_Invoice_Challan_Details.docm", b"MOCK_DOCM_VBA_MACRO_PAYLOAD")
    }
]


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic .eml test artifacts for Case File CA-ETI-01")
    parser.add_argument('--output-dir', default=os.path.join(os.path.dirname(__file__), 'sample_emails'),
                        help='Directory to write .eml files into (default: ./sample_emails)')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    print(f"[*] Generating {len(EMAILS_DATA)} sample .eml files into '{args.output_dir}'...")

    for item in EMAILS_DATA:
        msg = EmailMessage()
        msg['From']    = item['from']
        msg['To']      = item['to']
        msg['Subject'] = item['subject']
        msg['Date']    = item['date']
        msg['Authentication-Results'] = item['auth']
        msg['Received'] = item.get('received', '')

        if item.get('reply_to'):
            msg['Reply-To'] = item['reply_to']
        if item.get('cc'):
            msg['Cc'] = item['cc']

        msg.set_content(item['body'])

        if 'attachment' in item:
            fname, fdata = item['attachment']
            msg.add_attachment(fdata, maintype='application', subtype='octet-stream', filename=fname)

        out_path = os.path.join(args.output_dir, item['filename'])
        with open(out_path, 'wb') as f:
            f.write(msg.as_bytes())
        print(f" [+] Created {item['filename']}")

    print(f"\n[*] All {len(EMAILS_DATA)} .eml artifacts generated successfully.")


if __name__ == '__main__':
    main()
