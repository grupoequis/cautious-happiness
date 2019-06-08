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
    # Read from config file
    config = configparser.ConfigParser(allow_no_value=True)
    config.read("config.txt")
    c = imap4ssl.open_connection(config)
    #mailboxes.list_all(c)
    # Start the Idler thread
    idler = idle.Idler(c) # can changed to idler = idle.Idler(c, readonly=False) to mark messages as read
    idler.start()
    # Exit after 10 minutes
    time.sleep(600)
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
