import smtplib
from email.message import EmailMessage
import os

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

def send_otp_email(to_email, otp):
    msg = EmailMessage()
    msg["Subject"] = "GRIDCOINS OTP Verification"
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    
    # Beautiful Red and Black HTML Email
    msg.set_content(f"Your OTP is: {otp}")

    msg.add_alternative(f"""
    <html>
      <body style="background-color:black; color:red; padding:20px; font-family:Arial, sans-serif;">
        <h1 style="color:red;">Welcome to GRIDCOINS</h1>
        <p style="font-size:18px;">Your one-time password (OTP) is:</p>
        <h2 style="color:white; background-color:red; display:inline-block; padding:10px;">{otp}</h2>
        <p style="margin-top:30px;">Enter this OTP to verify your email and complete your signup process.</p>
        <hr style="border:1px solid red;">
        <p style="font-size:12px; color:grey;">GRIDCOINS - Securing your world with style.</p>
      </body>
    </html>
    """, subtype="html")
    
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)
