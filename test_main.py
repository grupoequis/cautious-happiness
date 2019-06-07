try:
    import imaplib2
except ImportError:
    raise SystemExit("Module imaplib2 is required (try <pip3 install ./imaplib2-master).")
try:
    import tkinter
except ImportError:
    raise SystemExit("Module tkinter is required.")
import imap4ssl
import idle
import mailboxes
import messages
import fetch_rfc822
import configparser
import time, os, sys
if (sys.maxsize <= 2**32):
    raise SystemExit("Program must run on a 64bit system.")

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
except KeyboardInterrupt:
    pass
finally:
    # Clean up.
    try:
        idler.stop()
        idler.join()
        c.logout()
    except:
        print("Couldn't join idler.")
