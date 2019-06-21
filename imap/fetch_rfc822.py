import imaplib2 as imaplib
import email
import email.parser
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
                rmessage.append(msg.get_body())

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
