import imaplib2, time
import server_connect
import threading
import message_mngr
import fetch_rfc822

# This is the threading object that does all the waiting on
# the event
class Idler(object):
    def __init__(self, connection):
        self.thread = threading.Thread(target=self.idle)
        self.connection = connection
        self.event = threading.Event()

    def start(self):
        print("Starting IDLE thread.")
        self.thread.start()

    def stop(self):
        self.event.set()

    def join(self):
        self.thread.join()

    def idle(self):
        # Starting an unending loop here
        while True:
            # if event was set on .stop()
            # then return
            if self.event.isSet():
                return
            # set needsync on false initially
            # to tell if an IDLE vent happenned
            self.needsync = False
            # Method called on IDLE event
            def callback(args):
                print(args)
                if not self.event.isSet():
                    self.needsync = True
                    self.event.set()
            # Do the actual idle call. Return immediately,
            # asynchronous return on callback
            self.connection.idle(callback=callback)
            # Wait until the thread event is set
            self.event.wait()
            # Act on whether there was an IDLE event
            # or the thread was stopped using .stop()
            if self.needsync:
                self.event.clear()
                self.dosync()
    # The method that gets called when a new email arrives.
    # Replace it with something better.
    def dosync(self):
        new_ids = message_mngr.get_inbox_ids(connection)[0].decode("utf-8").split()
        new_ids = [id for id in new_ids if id not in msg_ids]
        for id in new_ids:
            fetch_rfc822.fetch_message("INBOX", id, connection)

try:
    # Set the following two lines to your creds and server
    connection = server_connect.open_connection()
    msg_ids = message_mngr.get_inbox_ids(connection)[0].decode("utf-8").split()
    for id in msg_ids:
        fetch_rfc822.fetch_message("INBOX", id, connection)
    # We need to get out of the AUTH state, so we just select
    # the INBOX.
    connection.select("INBOX")
    # Start the Idler thread
    idler = Idler(connection)
    idler.start()
    # Because this is just an example, exit after 1 minute.
    time.sleep(3*60)
finally:
    # Clean up.
    idler.stop()
    idler.join()
    connection.close()
    # This is important!
    connection.logout()
