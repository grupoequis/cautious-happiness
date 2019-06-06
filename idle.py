import imaplib2, time
import imap4ssl
import threading
import messages
import fetch_rfc822

# This is the threading object that does all the waiting on
# the event
class Idler(object):
    def __init__(self, connection):
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
            for id in self.msg_ids:
                print(fetch_rfc822.fetch_message("INBOX", id, self.connection))
            # Starting an unending loop here
            while True:
                #Selecting mailbox to exit AUTH state
                self.connection.select("INBOX")
                # if event was set on .stop()
                # then return
                if self.event.isSet():
                    return
                # set needsync on false initially
                # to tell if an IDLE vent happenned
                self.needsync = False
                # Method called on IDLE event
                def callback(args):
                    #print(args)
                    if not self.event.isSet():
                        self.needsync = True
                        self.event.set()
                    # Do the actual idle call. Return immediately,
                    # asynchronous return on callback
                    self.connection.idle(callback=callback, timeout=1800)
                    # Wait until the thread event is set
                    self.event.wait()
                    # Act on whether there was an IDLE event
                    # or the thread was stopped using .stop()
                    if self.needsync:
                        self.event.clear()
                        self.dosync()
        except:
            self.stop()
    # The method that gets called when a new email arrives.
    # Replace it with something better.
    def dosync(self):
        response, new_ids = messages.get_ids(self.connection, flags = "UNSEEN")
        new_ids = new_ids[0].decode("utf-8").split()
        new_ids = [id for id in new_ids if id not in self.msg_ids]
        self.msg_ids = self.msg_ids + new_ids
        for id in new_ids:
            print(fetch_rfc822.fetch_message("INBOX", id, self.connection))
