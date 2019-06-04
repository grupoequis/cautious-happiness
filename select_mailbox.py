import imaplib2 as imaplib
from server_connect import open_connection

def mailbox_num_msg(mailbox_name, connection):
    response, data = connection.select(mailbox_name)
    num_msg = data[0]
    print("Response: {}. There are {} messages in {}".format(response, num_msg, mailbox_name))
