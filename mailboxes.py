import os
import imaplib2 as imaplib
import messages
import re #for easy parsing using regex

# Display number of messages in a given mailbox
def msgnum(mailbox_name, connection):
    response, data = connection.select(mailbox_name)
    num_msg = data[0]
    print("Response: {}. There are {} messages in {}".format(response, num_msg, mailbox_name))

# Display info about every mailbox
def list_all(connection):
    response, data = connection.list()
    print("Response code: {}".format(response))
    for line in data:
        flags, delimiter, mailbox_name = messages.__parse_list(line.decode("utf-8"))
        print(connection.status(mailbox_name, "(MESSAGES RECENT UIDNEXT UIDVALIDITY UNSEEN)"))
