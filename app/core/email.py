from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from app.models.user import User

# REPLACE THESE WITH YOUR CREDENTIALS
conf = ConnectionConfig(
    MAIL_USERNAME="raspberrypicourse5@gmail.com",
    MAIL_PASSWORD="ecww veph upin aarz", # Generate this in Google Security settings
    MAIL_FROM="raspberrypicourse5@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_otp_email(email: EmailStr, otp: str):
    message = MessageSchema(
        subject="Pulao King Verification Code",
        recipients=[email],
        body=f"<h3>Your Verification Code is: {otp}</h3><p>Use this to verify your account or reset your password.</p>",
        subtype=MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)