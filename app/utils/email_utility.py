# app/utils/email_utility.py
import smtplib
from email.message import EmailMessage
from utils.email_config import get_tenant_email_settings_by_api_key
from urllib.parse import urlparse

def make_brand_from_domain(website: str) -> str:
    """
    Converts domain like 'indianmountainrovers.com' -> 'Indian Mountain Rovers'
    Also handles full URLs like 'https://www.holidaysplanners.com'
    """
    if not website:
        return "Your Travel Brand"

    try:
        if "://" in website:
            domain = urlparse(website).netloc
        else:
            domain = website

        domain = domain.replace("www.", "")
        name_part = domain.split(".")[0]

        words = name_part.replace("-", " ").replace("_", " ").split()
        return " ".join(w.capitalize() for w in words)

    except:
        return "Your Travel Brand"


def send_email_dynamic(to_email: str, subject: str, body: str, api_key: str) -> bool:
    """
    Generic tenant-based email sender.
    """
    settings = get_tenant_email_settings_by_api_key(api_key)
    if not settings:
        print("Tenant email settings missing")
        return False

    smtp_host = settings["smtp_host"]
    smtp_port = settings["smtp_port"]
    smtp_username = settings["smtp_username"]
    smtp_password = settings["smtp_password"]

    if not smtp_host or not smtp_username or not smtp_password:
        print("Incomplete SMTP credentials")
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
        print("Email failed:", e)
        return False


# -------------------------------------------------------------
# ENQUIRY EMAIL
# -------------------------------------------------------------
def send_enquiry_email(enquiry: dict, api_key: str) -> bool:
    settings = get_tenant_email_settings_by_api_key(api_key)
    brand = make_brand_from_domain(settings.get("smtp_username", ""))

    user_email = enquiry.get("email")
    admin_email = settings.get("admin_email")

    # USER EMAIL (Beautiful)
    subject_user = f"✨ Thank You for Your Enquiry – {enquiry.get('destination','')}"

    body_user = f"""
Hi {enquiry.get('full_name','Traveller')} 👋,

Thank you for choosing **{brand}** for your upcoming trip! 🌍✈️  
We’ve successfully received your enquiry and our travel experts are already excited to help you plan an amazing experience.

📌 **Your Enquiry Summary**
• **Destination:** {enquiry.get('destination')}
• **Travel Date:** {enquiry.get('travel_date')}
• **Departure City:** {enquiry.get('departure_city')}
• **Travelers:** {enquiry.get('adults')} Adults, {enquiry.get('children')} Children, {enquiry.get('infants')} Infants
• **Hotel Preference:** {enquiry.get('hotel_category')}

💬 **Your Message:**  
{enquiry.get('additional_comments','No additional comments')}

Our team will reach out shortly with a personalised itinerary & quote.  
Thank you for trusting **{brand}** ❤️

Warm regards,  
**{brand} Travel Team**
"""

    send_email_dynamic(user_email, subject_user, body_user, api_key)

    # ADMIN EMAIL (with Brand in header)
    subject_admin = f"🔥 NEW ENQUIRY ALERT – {enquiry.get('destination')}"
    body_admin = f"""
🚨 **CRM Alert System – {brand}**

A new enquiry has just been submitted! 🎉  
Please follow up immediately for maximum conversion.

🧑‍💼 **Client Details**
• Name: {enquiry.get('full_name')}
• Email: {enquiry.get('email')}
• Phone: {enquiry.get('contact_number')}

🌎 **Trip Details**
• Destination: {enquiry.get('destination')}
• Travel Date: {enquiry.get('travel_date')}
• Departure City: {enquiry.get('departure_city')}
• Hotel Category: {enquiry.get('hotel_category')}
• Travelers: {enquiry.get('adults')} Adults, {enquiry.get('children')} Children, {enquiry.get('infants')} Infants

💬 Additional Notes:
{enquiry.get('additional_comments')}

⚡ Action Needed: Contact the client & prepare their quote!
"""

    send_email_dynamic(admin_email, subject_admin, body_admin, api_key)
    return True


# -------------------------------------------------------------
# BOOKING EMAIL
# -------------------------------------------------------------
def send_booking_email(booking: dict, api_key: str) -> bool:
    settings = get_tenant_email_settings_by_api_key(api_key)
    brand = make_brand_from_domain(settings.get("smtp_username", ""))

    user_email = booking.get("email")
    admin_email = settings.get("admin_email")

    # USER EMAIL
    subject_user = "🧾 Booking Request Received – Thank You!"

    body_user = f"""
Hi {booking.get('full_name','Traveller')} 🙌,

Great news! Your booking request has been received by **{brand}** 🎉  
Our team will reach out shortly to confirm availability and final details.

🧳 **Your Booking Summary**
• Departure Date: {booking.get('departure_date')}
• Sharing Option: {booking.get('sharing_option')}
• Adults: {booking.get('adults')}
• Children: {booking.get('children')}
• Total Estimate: ₹{booking.get('estimated_total_price')}

Thank you for choosing **{brand}** ❤️  
We’re excited to plan this amazing journey with you.

Warm regards,  
**{brand} Booking Team**
"""

    send_email_dynamic(user_email, subject_user, body_user, api_key)

    # ADMIN EMAIL
    subject_admin = f"🚨 NEW BOOKING REQUEST – {booking.get('full_name')}"
    body_admin = f"""
⚠️ **CRM Alert System – {brand}**

A client just submitted a *booking request* 🚀  
Please review & follow up immediately.

🧑‍💼 **Client:** {booking.get('full_name')}
📧 Email: {booking.get('email')}
📞 Phone: {booking.get('phone_number')}

🧳 **Booking Details**
• Date: {booking.get('departure_date')}
• Option: {booking.get('sharing_option')}
• Adults: {booking.get('adults')}
• Children: {booking.get('children')}
• Estimated Total: ₹{booking.get('estimated_total_price')}

⚡ Urgent: Contact the client ASAP.
"""

    send_email_dynamic(admin_email, subject_admin, body_admin, api_key)
    return True


# -------------------------------------------------------------
# TRIP INQUIRY EMAIL
# -------------------------------------------------------------
def send_trip_inquiry_email(inquiry: dict, api_key: str) -> bool:
    settings = get_tenant_email_settings_by_api_key(api_key)
    brand = make_brand_from_domain(settings.get("smtp_username", ""))

    user_email = inquiry.get("email")
    admin_email = settings.get("admin_email")

    subject_user = "📩 Your Trip Inquiry is Received!"
    body_user = f"""
Hello {inquiry.get('full_name','Traveller')} ✨,

Your trip inquiry has been successfully received by **{brand}**.

🧭 **Inquiry Details**
{inquiry}

Our team will call/email you shortly with customised travel options.

Warm regards,  
**{brand} Travel Team**
"""

    send_email_dynamic(user_email, subject_user, body_user, api_key)

    subject_admin = f"📢 New Trip Inquiry from {inquiry.get('full_name')}"
    body_admin = f"""
📣 **CRM Alert System – {brand}**

A new trip inquiry has been submitted.

Details:
{inquiry}

⚡ Action Required: Follow up with the client.
"""

    send_email_dynamic(admin_email, subject_admin, body_admin, api_key)
    return True
