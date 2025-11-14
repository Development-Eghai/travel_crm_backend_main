# app/utils/email_utility.py
import smtplib
from email.message import EmailMessage
from typing import Optional
from utils.email_config import get_tenant_email_settings_by_api_key

def send_email_dynamic(to_email: str, subject: str, body: str, api_key: str) -> bool:
    """
    Send an email using tenant SMTP settings found by api_key.
    Returns True on success, False otherwise.
    """
    if not api_key:
        print("send_email_dynamic: missing api_key")
        return False

    settings = get_tenant_email_settings_by_api_key(api_key)
    if not settings:
        print("send_email_dynamic: tenant SMTP config not found")
        return False

    smtp_host = settings.get("smtp_host")
    smtp_port = settings.get("smtp_port", 587)
    smtp_username = settings.get("smtp_username")
    smtp_password = settings.get("smtp_password")

    if not smtp_host or not smtp_username or not smtp_password:
        print("send_email_dynamic: incomplete SMTP configuration for tenant:", settings)
        return False

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = smtp_username
    msg["To"] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print("send_email_dynamic: failed to send:", e)
        return False


# Convenience wrappers for your app to call
def send_enquiry_email(enquiry_data: dict, api_key: str) -> bool:
    # customer confirmation
    customer_email = enquiry_data.get("email")
    subject_user = f"Thank you for your enquiry - {enquiry_data.get('destination','')}"
    body_user = f"""Hi {enquiry_data.get('full_name','Guest')},

Thank you for your enquiry about {enquiry_data.get('destination','your selected destination')}.
We received your request and our team will contact you soon.

Regards,
{enquiry_data.get('company_name','Team')}
"""
    sent = False
    if customer_email:
        sent = send_email_dynamic(customer_email, subject_user, body_user, api_key) or sent

    # admin notification
    settings = get_tenant_email_settings_by_api_key(api_key)
    admin_email = settings.get("admin_email") if settings else None
    subject_admin = f"New enquiry: {enquiry_data.get('destination','')}"
    body_admin = f"""
New enquiry received:

Name: {enquiry_data.get('full_name')}
Email: {enquiry_data.get('email')}
Phone: {enquiry_data.get('contact_number')}
Destination: {enquiry_data.get('destination')}
Comments: {enquiry_data.get('additional_comments')}
"""
    if admin_email:
        sent = send_email_dynamic(admin_email, subject_admin, body_admin, api_key) or sent

    return sent


def send_booking_email(booking: dict, api_key: str) -> bool:
    # customer confirmation
    customer_email = booking.get("email")
    subject_user = "Booking received"
    body_user = f"Hello {booking.get('full_name')},\n\nThanks — we received your booking request."

    sent = False
    if customer_email:
        sent = send_email_dynamic(customer_email, subject_user, body_user, api_key) or sent

    # admin notification
    settings = get_tenant_email_settings_by_api_key(api_key)
    admin_email = settings.get("admin_email") if settings else None
    subject_admin = f"Booking request from {booking.get('full_name')}"
    body_admin = f"""
Booking details:
Name: {booking.get('full_name')}
Phone: {booking.get('phone_number')}
Departure: {booking.get('departure_date')}
Total: {booking.get('estimated_total_price')}
"""
    if admin_email:
        sent = send_email_dynamic(admin_email, subject_admin, body_admin, api_key) or sent

    return sent


def send_trip_inquiry_email(inquiry: dict, api_key: str) -> bool:
    # customer confirmation
    customer_email = inquiry.get("email")
    subject_user = "Trip inquiry received"
    body_user = f"Hi {inquiry.get('full_name','Guest')},\n\nThanks for your inquiry."

    sent = False
    if customer_email:
        sent = send_email_dynamic(customer_email, subject_user, body_user, api_key) or sent

    # admin notification
    settings = get_tenant_email_settings_by_api_key(api_key)
    admin_email = settings.get("admin_email") if settings else None
    subject_admin = f"New trip inquiry from {inquiry.get('full_name')}"
    body_admin = f"Details: {inquiry}"
    if admin_email:
        sent = send_email_dynamic(admin_email, subject_admin, body_admin, api_key) or sent

    return sent
