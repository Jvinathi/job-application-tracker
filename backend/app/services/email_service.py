import resend
import os

resend.api_key = os.getenv("RESEND_API_KEY")

def send_reminder_email(to_email: str, company: str, role: str, reminder_type: str, note: str = None):
    try:
        params = {
            "from": "Job Tracker <onboarding@resend.dev>",
            "to": [to_email],
            "subject": f"[Job Tracker] Reminder: {reminder_type.replace('_', ' ').title()} — {role} at {company}",
            "html": f"""
            <div style="font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 20px;">
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
                        {'<tr><td style="padding:10px;font-weight:bold;">Note</td><td style="padding:10px;">' + str(note) + '</td></tr>' if note else ''}
                    </table>
                    <p style="color: #94a3b8; font-size: 12px;">
                        You set this reminder in Job Tracker.
                    </p>
                </div>
            </div>
            """
        }
        email = resend.Emails.send(params)
        print(f"✅ Email sent via Resend to {to_email} | ID: {email['id']}")
        return True
    except Exception as e:
        print(f"❌ Resend failed: {e}")
        return False