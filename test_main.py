import imap4ssl
import idle
import mailboxes
import messages
import fetch_rfc822
import configparser
import time, os, sys

try:
    import tkinter
except ImportError:
    raise SystemExit("Module tkinter is required.")
if (sys.maxsize <= 2**32):
    raise SystemExit("Program must run on a 64bit system.")
try:
    import imaplib2
except ImpotError:
    raise SystemExit("Module imaplib2 is required (try <pip3 install ./imaplib2-master).")

try:
    config = configparser.ConfigParser()
    config.read("../config.txt")
    c = imap4ssl.open_connection(config)
    # Set the following two lines to your creds and server
    #response, msg_ids = messages.get_ids(c, flags="UNSEEN")
    #msg_ids = msg_ids[0].decode("utf-8").split()
    #for id in msg_ids:
        #print(fetch_rfc822.fetch_message("INBOX", id, c))
    # We need to get out of the AUTH state, so we just select
    # the INBOX.
    #messages.search_all(c)
    # Start the Idler thread
    idler = idle.Idler(c)
    idler.start()
    # Because this is just an example, exit after 1 minute.
    time.sleep(900)
finally:
    # Clean up.
    try:
        idler.stop()
        idler.join()
    except:
        print("Couldn't join idler.")
    c.logout()
