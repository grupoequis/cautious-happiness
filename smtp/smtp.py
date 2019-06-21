import smtplib, email, os, base64
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


try:
    try:
        conn = smtplib.SMTP_SSL(host = 'smtp.gmail.com', timeout = 60)
    except smtplib.SMTPConnectError:
        raise ("Couldn't establish SMTP connection over SSL.")
    print("Connection to SMTP server established succesfully.")
    conn.set_debuglevel(2)
    try:
        conn.login('', '')
    except:
        pass
    print("Logged in to SMTP server succesfully.")

    ##creating mail
    msg = MIMEMultipart()
    msg.add_header("from", "")
    msg.add_header("to", "")
    msg.add_header("subject", "")
    msg.attach(MIMEText("", "plain"))

    files = ["att.txt"]
    for a_file in files:
        attachment = open(a_file, 'rb')
        file_name = os.path.basename(a_file)
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload(attachment.read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', 'attachment', filename= file_name)
        msg.attach(payload)


    conn.send_message(msg, '', '')


finally:
    conn.quit()
