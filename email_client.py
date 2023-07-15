import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail
import os
import streamlit as st

def send_email(email, subject, content):
    if os.environ.get('SEMDGRID_API_KEY') is not None:
        sendgrid_key = os.environ.get('SENDGRID_API_KEY')
    else:
        sendgrid_key = st.secrets['SENDGRID_API_KEY']

    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_key)
    from_email = Email("aivet@dvm.com")  # Replace with your SendGrid account email
    to_email = To(email)
    content = Content("text/plain", content)
    mail = Mail(from_email, to_email, subject, content)

    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        return response.status_code
    except Exception as e:
        return str(e)


