import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_reminder_email(to_email: str, company: str, role: str, reminder_type: str, note: str = None):
    subject = f"[Job Tracker] Reminder: {reminder_type.replace('_', ' ').title()} — {role} at {company}"

    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 20px;">
        <div style="background: #1E40AF; padding: 20px; border-radius: 8px 8px 0 0;">
            <h2 style="color: white; margin: 0;">Job Tracker Reminder</h2>
        </div>
        <div style="background: #f8fafc; padding: 24px; border: 1px solid #e2e8f0;">
            <p>Hi there! Here is your scheduled reminder:</p>
            <table style="width:100%; border-collapse:collapse;">
                <tr style="background:#e2e8f0;">
                    <td style="padding:10px; font-weight:bold;">Company</td>
                    <td style="padding:10px;">{company}</td>
                </tr>
                <tr>
                    <td style="padding:10px; font-weight:bold;">Role</td>
                    <td style="padding:10px;">{role}</td>
                </tr>
                <tr style="background:#e2e8f0;">
                    <td style="padding:10px; font-weight:bold;">Reminder</td>
                    <td style="padding:10px;">{reminder_type.replace('_', ' ').title()}</td>
                </tr>
                {'<tr><td style="padding:10px;font-weight:bold;">Note</td><td style="padding:10px;">' + str(note) + '</td></tr>' if note else ''}
            </table>
            <p style="color:#94a3b8; font-size:12px; margin-top:20px;">
                You set this reminder in Job Tracker.
            </p>
        </div>
    </div>
    """

    plain_body = f"Reminder: {reminder_type} for {role} at {company}."

    msg = MIMEMultipart('alternative')
    msg['From'] = f"Job Tracker <{EMAIL_ADDRESS}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(plain_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))

    # Try multiple ports
    ports_to_try = [
        ('smtp.gmail.com', 587, 'STARTTLS'),
        ('smtp.gmail.com', 465, 'SSL'),
        ('smtp.gmail.com', 25, 'PLAIN'),
    ]

    for host, port, method in ports_to_try:
        try:
            if method == 'STARTTLS':
                with smtplib.SMTP(host, port, timeout=10) as server:
                    server.ehlo()
                    server.starttls()
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
            elif method == 'SSL':
                import ssl
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(host, port, context=context, timeout=10) as server:
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
            else:
                with smtplib.SMTP(host, port, timeout=10) as server:
                    server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())

            print(f"✅ Email sent to {to_email} via {host}:{port} ({method})")
            return True
        except Exception as e:
            print(f"❌ Port {port} ({method}) failed: {e}")
            continue

    # Last resort — use Resend but to registered email only
    print(f"⚠️ All SMTP ports blocked. Sending to registered Resend email instead.")
    try:
        import resend
        resend.api_key = os.getenv("RESEND_API_KEY")
        params = {
            "from": "Job Tracker <onboarding@resend.dev>",
            "to": ["reddyvinathi3@gmail.com"],  # resend free tier limitation
            "subject": subject,
            "html": html_body + f"<p><strong>Originally for: {to_email}</strong></p>"
        }
        resend.Emails.send(params)
        print(f"✅ Sent to Resend fallback email (intended for {to_email})")
        return True
    except Exception as e:
        print(f"❌ Resend also failed: {e}")
        return False