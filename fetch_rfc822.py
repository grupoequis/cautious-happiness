import imaplib2 as imaplib
import email
import email.parser
from email import policy

def fetch_message(mailbox_name, msgid, connection):
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
            #rmessage.append(msg.get_body())

    connection.close()

    return typ, rmessage
