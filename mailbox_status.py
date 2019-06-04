import os
import imaplib2 as imaplib
from server_connect import open_connection
from list_mailboxes import parse_list_response

#mailboxes = []
def list_status_all(connection):
    response, data = connection.list()
    print("Response code: {}".format(response))
    for line in data:
        flags, delimiter, mailbox_name = parse_list_response(line.decode("utf-8"))
        #mailboxes.append([flags, delimiter, mailbox_name])
        print(connection.status(mailbox_name, "(MESSAGES RECENT UIDNEXT UIDVALIDITY UNSEEN)"))
