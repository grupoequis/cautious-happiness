import imaplib2 as imaplib
import email
import email.parser
import os
from email import policy

# Fetch a message's data as described in RFC822
def fetch_message(mailbox_name, msgid, connection, body=False):
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
            print(str(save_attachment(msg, "/home/efrain/Desktop/attachments")))
            
    connection.close()

    return typ, rmessage

def fetch_message_print(mailbox_name, msgid, connection, body=False):
    response, message = fetch_message(mailbox_name, msgid, connection, body)
    print("{:^8}: {}".format("SUBJECT", message[0]))
    print("{:^8}: {}".format("TO", message[1]))
    print("{:^8}: {}".format("FROM", message[2]))
    if body:
        print("{:^8}: {}".format("BODY:", message[3]))
    print("----------------")

def save_attachment(msg, download_folder="/tmp"):
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
            att_path = os.path.join(download_folder, filename)
            paths.append(att_path)

            if not os.path.isfile(att_path):
                fp = open(att_path, 'wb+')
                fp.write(part.get_payload(decode=True))
                fp.close()
        return paths
