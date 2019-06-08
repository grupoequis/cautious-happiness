import imaplib2, time, sys
import imap4ssl
import threading
import messages
import fetch_rfc822
# IDLE threaded class implementation based on Tim Stoop's
# Python: IMAP IDLE with imaplib2 post at blog.timstoop.com

# This is the threading object that does all the waiting on
# the event
class Idler(object):
    def __init__(self, connection, readonly=True, body=False):
        self.body = body
        self.readonly = readonly
        self.thread = threading.Thread(target=self.idle)
        self.connection = connection
        self.event = threading.Event()
        response, self.msg_ids = messages.get_ids(self.connection, flags = "UNSEEN")
        self.msg_ids = self.msg_ids[0].decode("utf-8").split()

    def start(self):
        print("Starting IDLE thread.")
        self.thread.start()

    def stop(self):
        self.event.set()

    def join(self):
        self.thread.join()

    def idle(self):
        try:
            print("Fetching UNREAD messages:")
            for id in self.msg_ids:
                fetch_rfc822.fetch_message_print("INBOX", id, self.connection, self.body)
                self.connection.select("INBOX")
                if not self.readonly:
                    self.connection.store(id, '+FLAGS', '\Seen')
            # Starting an unending loop here
            while True:
                # if event was set on .stop()
                # then return
                if self.event.isSet():
                    return
                # set needsync on false initially
                # to tell if an IDLE event happenned
                self.needsync = False
                # Method called on IDLE event
                def callback(args):
                    #print(args)
                    if not self.event.isSet():
                        self.needsync = True
                        self.event.set()
                #Selecting mailbox to exit AUTH state
                self.connection.select("INBOX")
                # Do the actual idle call. Return immediately,
                # asynchronous return on callback
                # timeout is 29min by default.
                print("Idling...")
                self.connection.idle(callback=callback, timeout=30)
                # Wait until the thread event is set
                self.event.wait()
                # Act on whether there was an IDLE event
                # or the thread was stopped using .stop()
                if self.needsync:
                    self.event.clear()
                    self.dosync()
        except KeyboardInterrupt:
            pass
    # Method that gets called when a new message arrives
    def dosync(self):
        response, new_ids = messages.get_ids(self.connection, flags = "UNSEEN")
        new_ids = new_ids[0].decode("utf-8").split()
        new_ids = [id for id in new_ids if id not in self.msg_ids]
        self.msg_ids = self.msg_ids + new_ids
        for id in new_ids:
            print("New mail!!!")
            fetch_rfc822.fetch_message_print("INBOX", id, self.connection, self.body)
            if not self.readonly:
                self.connection.store(id, '+FLAGS', '\Seen')
