import os
import imaplib2 as imaplib
import re #for easy parsing using regex

def __parse_list(line):
    #Set pattern for imap4.list() response
    list_response_pattern = re.compile(r"\((?P<flags>.*)\) \"(?P<delimiter>.*)\" (?P<name>.*)") #pattern for parsing binary
    #Match line with pattern, return each section as a tuple
    flags, delimiter, mailbox_name = list_response_pattern.match(line).groups()
    #strip quotes from mailbox name
    mailbox_name = mailbox_name.strip(r'"')
    return (flags, delimiter, mailbox_name)

def msgnum(mailbox_name, connection):
    response, data = connection.select(mailbox_name)
    num_msg = data[0]
    print("Response: {}. There are {} messages in {}".format(response, num_msg, mailbox_name))

#mailboxes = []
def list_all(connection):
    response, data = connection.list()
    print("Response code: {}".format(response))
    for line in data:
        flags, delimiter, mailbox_name = __parse_list(line.decode("utf-8"))
        #mailboxes.append([flags, delimiter, mailbox_name])
        print(connection.status(mailbox_name, "(MESSAGES RECENT UIDNEXT UIDVALIDITY UNSEEN)"))
