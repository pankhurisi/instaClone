# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from sendgrid.helpers.mail import *


def send_response(post_url):
    sg = sendgrid.SendGridAPIClient(apikey='SEND_GRID_KEY')
    receipt = "pankhurisingh19ju@gmail.com" # email-id
    from_email = Email("pankhurisingh@mrei.ac.in")
    to_email = Email(receipt)
    content_message = "<html><body><img src =" + post_url + "</body></html>"
    print content_message
    subject = "Image of dirty area"
    content = Content("text/html", content_message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)