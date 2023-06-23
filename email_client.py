import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail
import os

def send_email(email, subject, content):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("ravi@tolwani.com")  # Replace with your SendGrid account email
    to_email = To(email)
    content = Content("text/plain", content)
    mail = Mail(from_email, to_email, subject, content)

    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        return response.status_code
    except Exception as e:
        return str(e)


