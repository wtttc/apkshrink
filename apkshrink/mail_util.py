#! /usr/bin/env python
# -*- coding: utf-8 -*-
from email.mime.application import MIMEApplication

__author__ = 'tiantong'

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

SMPT_URL = ""
SMPT_PORT = 0

# MIMEText should has been used on mail_content
def sendMail(mail_content, email_from, email_to, user_name, password, list_to_send):
    emailto = email_to
    emailfrom = email_from

    message = MIMEMultipart('alternative')
    message['To'] = ", ".join(emailto)
    message['From'] = emailfrom
    message['Subject'] = 'Test email'

    storeplain = MIMEText(mail_content, 'plain')
    plaintextemailmessage = unicode(storeplain)

    storeplain = MIMEText(plaintextemailmessage, 'plain')
    message.attach(storeplain)

    for key in list_to_send:
        part = MIMEApplication(open(key, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=key)
        message.attach(part)

    deetsurl = smtplib.SMTP(SMPT_URL, SMPT_PORT)
    deetsuser = user_name
    deetspassword = password

    deetsurl.ehlo()
    deetsurl.starttls()
    deetsurl.ehlo()
    deetsurl.login(deetsuser, deetspassword)

    deetsurl.sendmail(emailfrom, emailto, message.as_string())

    deetsurl.quit()
