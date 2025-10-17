import os
import smtplib
from email.message import EmailMessage

# load_dotenv()

SMTP_HOST = "smtp.zoho.in"
SMTP_PORT = 587
ZOHO_USERNAME = "sales@indianmountainrovers.com"
ZOHO_PASSWORD = "W5mSWcxnamrH"

def send_enquiry_email(enquiry_data: dict):
    msg = EmailMessage()
    msg["Subject"] = f"Your Kerala trip enquiry confirmation"
    msg["From"] = ZOHO_USERNAME
    msg["To"] = enquiry_data.get("email", "support@yourdomain.com")

    msg.set_content(f"""
Hi {enquiry_data.get("full_name", "Guest")},

Thank you for your enquiry about traveling to {enquiry_data.get("destination", "your selected destination")}!

Here are the details you submitted:
- Departure City: {enquiry_data.get("departure_city", "N/A")}
- Travel Date: {enquiry_data.get("travel_date", "N/A")}
- Adults: {enquiry_data.get("adults", 0)}
- Children: {enquiry_data.get("children", 0)}
- Infants: {enquiry_data.get("infants", 0)}
- Hotel Category: {enquiry_data.get("hotel_category", "N/A")}
- Contact Number: {enquiry_data.get("contact_number", "N/A")}
- Additional Comments: {enquiry_data.get("additional_comments", "None")}

Our team will get back to you shortly with a customized itinerary and pricing.

Warm regards,  
Yaadigo Travel Team
""")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(ZOHO_USERNAME, ZOHO_PASSWORD)
        server.send_message(msg)


def send_trip_inquiry_email(inquiry: dict):
    print("Sending email to:", inquiry.get("email"))
    msg = EmailMessage()
    msg["Subject"] = "Your Trip Inquiry Confirmation"
    msg["From"] = ZOHO_USERNAME
    msg["To"] = inquiry.get("email", "support@yourdomain.com")

    msg.set_content(f"""
Hi {inquiry.get("full_name", "Guest")},

Thank you for submitting your trip inquiry! We're excited to help you plan your journey.

Here are the details you provided:
- Departure Date: {inquiry.get("departure_date", "N/A")}
- Adults: {inquiry.get("adults", 0)}
- Children: {inquiry.get("children", 0)}
- Children's Ages: {', '.join(map(str, inquiry.get("children_ages", [])))}
- Phone Number: {inquiry.get("phone_number", "N/A")}

Our travel team will reach out to you shortly with personalized options.

Warm regards,  
Yaadigo Travel Team
""")

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(ZOHO_USERNAME, ZOHO_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print("Email sending failed:", e)  # ✅ Log the error


def send_booking_email(booking: dict):
    msg = EmailMessage()
    msg["Subject"] = "Your Booking Confirmation"
    msg["From"] = ZOHO_USERNAME
    msg["To"] = booking.get("email", "support@yourdomain.com")

    msg.set_content(f"""
Hi {booking.get("full_name", "Guest")},

Thank you for submitting your booking request! We're excited to help you finalize your travel plans.

Here are the details you provided:
- Departure Date: {booking.get("departure_date", "N/A")}
- Sharing Option: {booking.get("sharing_option", "N/A")}
- Price per Person: ₹{booking.get("price_per_person", 0):,.2f}
- Adults: {booking.get("adults", 0)}
- Children: {booking.get("children", 0)}
- Estimated Total Price: ₹{booking.get("estimated_total_price", 0):,.2f}
- Phone Number: {booking.get("phone_number", "N/A")}

Our team will contact you shortly to confirm availability and next steps.

Warm regards,  
Yaadigo Travel Team
""")

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(ZOHO_USERNAME, ZOHO_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print("Email sending failed:", e)

