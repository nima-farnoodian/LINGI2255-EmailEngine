# -*- coding: utf-8 -*-
"""

@author: Nima
"""

import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


password = '-----------'
directory='C:/EmailTest/'
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]

sender_email = "a gmail email for test @gmail.com"
receiver_email = "Your email meant to receive the emails from clients"
for filename in onlyfiles:
    print ("File " + filename + " is being sent" )
    subject = "Nima Farnoodian Telegram_" + filename
    body = "This is the file " + filename + " which has been sent from Nima Farnoodian Telegrams"

    
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    
    # Open PDF file in binary mode
    with open(directory+filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    
    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)
    
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text
