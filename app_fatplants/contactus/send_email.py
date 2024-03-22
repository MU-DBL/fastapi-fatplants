from typing import List
from fastapi import FastAPI, UploadFile, File, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from Google import Create_Service
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText  # Add this import statement
import base64

router = APIRouter(
    tags=["contactus"],
    # dependencies=[Depends(jwt.JWTBearer())],
    responses={404: {"description": "Error in calling species API"}},
)

# CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = Create_Service(API_NAME, API_VERSION, SCOPES)

@router.post("/send_email/")
async def send_email(request: Request, attachments: List[UploadFile] = File(default=[])):
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
            <img src="https://digbio.missouri.edu/wp-content/uploads/2022/07/DBL-500-%C3%97-350-px-4-300x210.png" width=120px height=84px> </img>
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
    mimeMessage['to'] = 'fatplantsmu@gmail.com' 
    mimeMessage['From'] = 'FatPlants MU <fatplantsmu@gmail.com>'
    mimeMessage['subject'] = email_subject
    mimeMessage.attach(MIMEText(emailMsg, 'html'))
    
    if attachments:
        for attachment in attachments:
            attached_file = MIMEApplication(attachment.file.read(), _subtype='octet-stream')
            attached_file.add_header('Content-Disposition', 'attachment', filename=attachment.filename)
            mimeMessage.attach(attached_file)
    
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()

    return {'message': 'Email sent successfully!'}


