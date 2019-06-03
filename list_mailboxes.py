import imaplib #IMAP4
import os #path functions
import re #for easy parsing using regex
from server_connect import open_connection #open connection as set by config.txt

list_response_pattern = re.compile(r"\((?P<flags>.*)\) \"(?P<delimiter>.*)\" (?P<name>.*)") #pattern for parsing binary

def parse_list_response(line):
    #Match line with pattern, return each section as a tuple
    flags, delimiter, mailbox_name = list_response_pattern.match(line).groups()
    #strip quotes from mailbox name
    mailbox_name = mailbox_name.strip(r'"')
    return (flags, delimiter, mailbox_name)
