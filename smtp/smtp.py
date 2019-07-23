import smtplib, email, os, base64
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import url

try:
    try:
        conn = smtplib.SMTP_SSL(host = 'smtp.gmail.com', timeout = 60)
    except smtplib.SMTPConnectError:
        raise ("Couldn't establish SMTP connection over SSL.")
    print("Connection to SMTP server established succesfully.")
    conn.set_debuglevel(2)
    username =
    password =
    sender =
    receiver =
    subject = 
    try:
        conn.login(username, password)
    except:
        pass
    print("Logged in to SMTP server succesfully.")

    ##creating mail
    msg = MIMEMultipart()
    msg.add_header("from", sender)
    msg.add_header("to", receiver)
    msg.add_header("subject", subject)
    msg.attach(MIMEText(message, "plain"))

    files = []
    for a_file in files:
        attachment = open(a_file, 'rb')
        file_name = os.path.basename(a_file)
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload(attachment.read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', 'attachment', filename= file_name)
        msg.attach(payload)

    if len(msg.as_string()) > 25000000:
        print("Size is larger than 25MB. Proceed?")
        if input() == 'n':
            exit()

    lowrep = url.get_rep(msg.as_string()+' '+subject)
    if lowrep:
        for url in lowrep:
        print("url "+url+" is non trusted. Proceed?")
        if input() == 'n':
            exit()
    conn.send_message(msg, username, receiver)

finally:
    conn.quit()
