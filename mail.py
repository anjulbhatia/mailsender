from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def prompt_continuation(width, line_number, wrap_count):
    if wrap_count > 0:
        return " " * (width - 3) + "-> "
    else:
        text = ("- %i - " % (line_number + 1)).rjust(width)
        return HTML("<strong>%s</strong>") % text

#Take User inputs
email_address = prompt('Email: ')
password = prompt('Password: ', is_password=True)
recipients = prompt('Recipient(s): ').split(',')
subject = prompt('Subject: ')
message = prompt("Message: ", multiline=True, prompt_continuation=prompt_continuation, 
    bottom_toolbar=HTML('<b>Press [Esc] followed by [Enter] to end message.</b>'))
filename = prompt('Attachment: ')

try:
    #STMP Client setup and sending message
    smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
    smtp_ssl_port = 465

    message_content = MIMEMultipart()
    message_content['Subject'] = subject
    message_content['From'] = email_address
    message_content['To'] = ', '.join(recipients)
    message_content.attach(MIMEText(message, 'plain'))

    #Adding Attachment
    try:
        if filename not in ["", " ", None]:
            attachment = open(filename, "rb")
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            message_content.attach(p)
    except:
        print("Attachment not found")

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(email_address, password)
    server.sendmail(email_address, recipients, message_content.as_string())
    server.quit()

    print("Email sent successfully")

except:
    print('''Email not sent! Try Changing your mail settings to allow less secure apps
Or Contact the developer at anjulbhatia2003@gmail.com''')