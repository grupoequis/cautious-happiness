import smtplib, email, os, base64
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import url

class smtp(object):
    """docstring for ClassName"""
    def __init__(self):
        self.conn = None
        
    def connection(self,username,password):
        try:
            self.conn = smtplib.SMTP_SSL(host = 'smtp.gmail.com', timeout = 60)
        except smtplib.SMTPConnectError:
            raise ("Couldn't establish SMTP connection over SSL.")
        print("Connection to SMTP server established succesfully.")
        try:
            self.conn.login(username, password)
        except:
            pass
        print("Logged in to SMTP server succesfully.")

    def checkMessage(self,sender,receiver,subject,message,files):
        ##creating mail
        msg = MIMEMultipart()
        msg.add_header("from", sender)
        msg.add_header("to", receiver)
        msg.add_header("subject", subject)
        msg.attach(MIMEText(message, "plain"))
        i = 0
        for a_file in files:
            #attachment = open(a_file, 'rb')
            #file_name = os.path.basename(a_file)
            payload = MIMEBase('application', 'octate-stream')
            #payload.set_payload(attachment.read())
            payload.set_payload(a_file[0])
            encoders.encode_base64(payload)
            payload.add_header('Content-Disposition', 'attachment', filename= a_file[1])
            msg.attach(payload)
        urls = url.get_urls(msg.as_string()+' '+subject)
        lowrep = url.get_rep(message+' '+subject)
        limitsize=0
        if len(msg.as_string()) > 25000000:
            limitsize=1

        return lowrep,limitsize,msg

    def sendMessage(self,msg,sender,receiver) :
        self.conn.send_message(msg, sender, receiver)
            #url.reputation("google.com")
            #urls = url.get_urls(msg.as_string()+' '+subject)
        
        
        #lowrep = url.get_rep(message+' '+subject)
        #for url in lowrep:
        #    print("url "+url+" is non trusted. Proceed?")
        #    if input() == 'n':
        #        exit()

       # if len(msg.as_string()) > 25000000:
       #     print("Size is larger than 25MB. Proceed?")
       #     if input() == 'n':
       #         exit()
