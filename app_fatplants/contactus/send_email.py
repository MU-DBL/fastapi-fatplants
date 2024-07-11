from typing import List
from fastapi import UploadFile, File, Request, APIRouter
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from auth.credentials import gmail_api_credentials

router = APIRouter(
    tags=["contactus"],
    responses={404: {"description": "Error in calling species API"}},
)

try:
    from_addr = gmail_api_credentials['email']
    password = gmail_api_credentials['appPassword']

except Exception as e:
    print('Unable to read credentials', e)

@router.post("/send_email/")
async def send_email(request: Request, attachments: List[UploadFile] = File(default=[])):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_addr, password) 
        data = await request.form()
        firstName = data.get('firstName')
        lastName = data.get('lastName')
        subject = data.get('subject')
        email_subject = f'New Communication from {firstName} {lastName}'
        message_body = data.get('message')
        guest_email = data.get('email')

        emailMsg = f"""
        <html>
        <head></head>
        <body style="font-family: Arial, sans-serif;">
            <div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px;">
                <h2>{subject}</h2>
                <div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px;">
                    <p>{message_body}</p>
                </div>
                <br>
                Reply to them at <a href="mailto:{guest_email}">{guest_email}</a>
            </div>
        </body>
        </html>
        """

        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = from_addr  
        mimeMessage['From'] = f'FatPlants MU <{from_addr}>'  
        mimeMessage['subject'] = email_subject
        mimeMessage.attach(MIMEText(emailMsg, 'html'))

        for attachment in attachments:
            attached_file = MIMEApplication(await attachment.read(), _subtype='octet-stream')
            attached_file.add_header('Content-Disposition', 'attachment', filename=attachment.filename)
            mimeMessage.attach(attached_file)

        server.send_message(mimeMessage)
        server.quit()
        return {'message': 'Email sent successfully!'}

    except Exception as e:
        print(f"Failed to send email: {e}")
        return {"message": f"Failed to send email: {e}"}
