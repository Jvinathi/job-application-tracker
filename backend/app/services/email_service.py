import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import EMAIL_ADDRESS, EMAIL_PASSWORD

def send_reminder_email(to_email: str, company: str, role: str, reminder_type: str, note: str = None):
    subject = f"[Job Tracker] Reminder: {reminder_type.replace('_', ' ').title()} — {role} at {company}"

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 20px;">
        <div style="background: #1E40AF; padding: 20px; border-radius: 8px 8px 0 0;">
            <h2 style="color: white; margin: 0;">Job Tracker Reminder</h2>
        </div>
        <div style="background: #f8fafc; padding: 24px; border: 1px solid #e2e8f0; border-radius: 0 0 8px 8px;">
            <p style="color: #334155;">Hi there! Here is your scheduled reminder:</p>
            <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
                <tr style="background: #e2e8f0;">
                    <td style="padding: 10px; font-weight: bold;">Company</td>
                    <td style="padding: 10px;">{company}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; font-weight: bold;">Role</td>
                    <td style="padding: 10px;">{role}</td>
                </tr>
                <tr style="background: #e2e8f0;">
                    <td style="padding: 10px; font-weight: bold;">Reminder</td>
                    <td style="padding: 10px;">{reminder_type.replace('_', ' ').title()}</td>
                </tr>
                {'<tr><td style="padding:10px;font-weight:bold;">Note</td><td style="padding:10px;">' + note + '</td></tr>' if note else ''}
            </table>
            <p style="color: #94a3b8; font-size: 12px;">
                You set this reminder in Job Tracker. To stop reminders, delete them from the app.
            </p>
        </div>
    </body>
    </html>
    """

    plain_body = f"Reminder: {reminder_type} for {role} at {company}. Note: {note or 'None'}"

    msg = MIMEMultipart('alternative')
    msg['From'] = f"Job Tracker <{EMAIL_ADDRESS}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(plain_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))

    # Try port 587 with STARTTLS first
    try:
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print(f"Email sent via port 587 to {to_email}")
        return True
    except Exception as e1:
        print(f"Port 587 failed: {e1}")
        # Try port 465 SSL as fallback
        try:
            import ssl
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context, timeout=30) as server:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
            print(f"Email sent via port 465 to {to_email}")
            return True
        except Exception as e2:
            print(f"Port 465 also failed: {e2}")
            return False