# import smtplib
# import os
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, EmailStr
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv

# load_dotenv()

# app = FastAPI()

# # CORS - Allow frontend to connect

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173",           # Local testing
#         "http://127.0.0.1:5173",           # Local testing IP
#         "https://gaurisagarportfolio.vercel.app"  # <-- YE LINE ADD KAREIN (Aapka Vercel Domain)
#     ],
#     allow_credentials=True,
#     allow_methods=["POST"],  # Ya ["*"] kar dein agar future mein aur methods chahiye
#     allow_headers=["*"],
# )

# # Data validation
# class ContactForm(BaseModel):
#     name: str
#     email: EmailStr
#     message: str

# # Send email function
# def send_email(data: ContactForm):
#     sender = os.getenv("GMAIL_USER")
#     password = os.getenv("GMAIL_APP_PASSWORD")
#     receiver = os.getenv("GMAIL_USER")  # Send to yourself

#     subject = f"Portfolio Contact: {data.name}"
#     body = f"""
# New message from your portfolio!

# Name: {data.name}
# Email: {data.email}

# Message:
# {data.message}
# """

#     msg = MIMEMultipart()
#     msg['From'] = sender
#     msg['To'] = receiver
#     msg['Subject'] = subject
#     msg.attach(MIMEText(body, 'plain'))

#     try:
#         server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#         server.login(sender, password)
#         server.sendmail(sender, receiver, msg.as_string())
#         server.quit()
#         return True
#     except Exception as e:
#         print(f"❌ Email error: {e}")
#         return False

# # API endpoint
# @app.post("/contact")
# async def handle_contact(form: ContactForm):
#     print(f"📩 Received from: {form.name}")
    
#     success = send_email(form)
    
#     if success:
#         return {"message": "Email sent successfully"}
#     else:
#         raise HTTPException(status_code=500, detail="Failed to send email")










from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# --- UPDATE THIS PART ---
# CORS Middleware - Sabhi origins ko allow karne ke liye "*" use karein
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" ka matlab hai koi bhi frontend isse connect kar sakta hai
    allow_credentials=False, # Wildcard "*" ke sath credentials False hona chahiye
    allow_methods=["*"],
    allow_headers=["*"],
)
# ------------------------

# Data Validation
class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

# Email Logic
def send_email(data: ContactForm):
    sender = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_APP_PASSWORD")
    receiver = os.getenv("GMAIL_USER")

    if not sender or not password:
        print("❌ Error: GMAIL_USER or GMAIL_APP_PASSWORD not found in .env")
        return False

    subject = f"Portfolio Contact: {data.name}"
    body = f"""
New message from portfolio!

Name: {data.name}
Email: {data.email}

Message:
{data.message}
"""

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Email error: {e}")
        return False

@app.post("/contact")
async def handle_contact(form: ContactForm):
    print(f"📩 Received data: {form}") # Debugging ke liye print
    
    success = send_email(form)
    
    if success:
        return {"message": "Email sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email")