import imaplib
import email
import email.parser
from email import policy
import server_connect as imaplib_connect

def fetch_message(mailbox_name, msgid, connection):
#with imaplib_connect.open_connection() as connection:
    connection.select(mailbox_name, readonly=True)

    typ, msg_data = connection.fetch(msgid, '(RFC822)')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            email_parser = email.parser.BytesFeedParser(policy = policy.default)
            email_parser.feed(response_part[1])
            msg = email_parser.close()
            #body = msg.get_body()
            #print(msg)
            msg.set_default_type("text/plain")
            for header in ['subject', 'to', 'from']:
                print('{:^8}: {}'.format(
                    header.upper(), msg[header]))
            print('{:^8}: {}'.format('BODY', msg['content-type']))
            print(msg.get_body())
