import imaplib
import server_connect
from list_mailboxes import parse_list_response

def search_all(connection):
    response, mbox_data = connection.list()
    for line in mbox_data:
        flags, delimiter, mbox_name = parse_list_response(line.decode("utf-8"))
        if("\\Noselect" in flags):
            continue
        connection.select("{}".format(mbox_name), readonly=True)
        response, msg_ids = connection.search(None, "ALL")
        print(mbox_name, response, msg_ids)
