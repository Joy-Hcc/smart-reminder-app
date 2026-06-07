import logging
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import get_settings

logger = logging.getLogger(__name__)


def send_reminder_email(to_email: str, title: str, category: str, description: str | None, priority: str) -> tuple[bool, str]:
    settings = get_settings()
    if not settings.sendgrid_api_key:
        return False, "SendGrid API key not configured"

    sg = SendGridAPIClient(settings.sendgrid_api_key)
    content = f"""【智能提醒】{category} - {title}

时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
优先级：{priority}

{description or ''}

---
此邮件由智能提醒App自动发送
"""
    message = Mail(
        from_email=settings.sendgrid_from_email,
        to_emails=to_email,
        subject=f"【智能提醒】{category} - {title}",
        plain_text_content=content,
    )
    try:
        response = sg.send(message)
        success = response.status_code in (200, 202)
        if not success:
            logger.warning("SendGrid returned status %d for %s", response.status_code, to_email)
        return success, f"status_{response.status_code}"
    except Exception:
        logger.error("Failed to send email to %s", to_email, exc_info=True)
        return False, "Email delivery failed"
