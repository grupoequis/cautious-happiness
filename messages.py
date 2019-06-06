import imaplib2 as imalib
import re #for easy parsing using regex

def __parse_list(line):
    #Set pattern for imap4.list() response
    list_response_pattern = re.compile(r"\((?P<flags>.*)\) \"(?P<delimiter>.*)\" (?P<name>.*)") #pattern for parsing binary
    #Match line with pattern, return each section as a tuple
    flags, delimiter, mailbox_name = list_response_pattern.match(line).groups()
    #strip quotes from mailbox name
    mailbox_name = mailbox_name.strip(r'"')
    return (flags, delimiter, mailbox_name)

def search_all(connection):
    response, mbox_data = connection.list()
    for line in mbox_data:
        flags, delimiter, mbox_name = __parse_list(line.decode("utf-8"))
        response, msg_ids = get_ids(connection, mbox_name, "ALL")
        print(mbox_name, response, msg_ids)

def get_ids(connection, mailbox="INBOX", flags="ALL"):
    response, last_id = connection.select(mailbox, readonly=True)
    if(response == "NO"):
        return response, last_id
    response, msg_ids = connection.search(None, flags)
    connection.close()
    return response, msg_ids
