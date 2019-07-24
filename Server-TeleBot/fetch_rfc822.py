import imaplib2 as imaplib
import email
import email.parser
import os
from email import policy
class fetch(object):
    
    def __init__(self):
        self.emails = []
        self.attach = []
        self.i = 0

    # Fetch a message's data as described in RFC822
    def fetch_message(self,mailbox_name, msgid, connection, body=True):
    #with imaplib_connect.open_connection() as connection:
        connection.select(mailbox_name, readonly=True)
        rmessage = []
        typ, msg_data = connection.fetch(msgid, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                email_parser = email.parser.BytesFeedParser(policy = policy.default)
                email_parser.feed(response_part[1])
                msg = email_parser.close()
                msg.set_default_type("text/plain")
                for header in ['subject', 'to', 'from']:
                    rmessage.append(msg[header])
                if body:
                    rmessage.append(msg.get_body(preferencelist=('plain', 'html')).get_content())
                address="/tmp"
                dirAddres=self.save_attachment(msg, address)
                if (dirAddres!=[]):
                    self.i=self.i+1
                self.attach.append(dirAddres)
                
                

        connection.close()

        return typ, rmessage

    def fetch_message_print(self,mailbox_name, msgid, connection, body=True):
        response, message = self.fetch_message(mailbox_name, msgid, connection, body)
        str1="{:^8}: {}".format("SUBJECT", message[0])
        str2="{:^8}: {}".format("TO", message[1])
        str3=str1+'\n'+str2+'\n'+"{:^8}: {}".format("FROM", message[2])
        if body:
            str3=str3+'\n'+"{:^8}: {}".format("BODY", message[3])
        self.emails.append(str3)
        print(str3)
        print("----------------")
        
    def save_attachment(self,msg, download_folder="/tmp"):
            """
            Given a message, save its attachments to the specified
            download folder (default is /tmp)

            return: file path to attachment
            """
            paths = []
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()
                filename="["+"#"+str(self.i)+']'+filename
                att_path = os.path.join(download_folder, filename)
                paths.append(att_path)
                if not os.path.isfile(att_path):
                    fp = open(att_path, 'wb+')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
            return paths

    