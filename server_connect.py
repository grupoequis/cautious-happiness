import imaplib
import configparser
import os

def open_connection():
    #Read the config file
    config = configparser.ConfigParser()
    config.read(os.path.expanduser("~/Desktop/IMAPClient/config.txt"))
    print(config.sections())

    #Connect to server
    hostname = config['server']['hostname']
    port = config['server']['port']
    print ("Connecting to " + hostname)
    connection = imaplib.IMAP4_SSL(host=hostname)

    #Login to account
    username = config['account']['username']
    password = config['account']['password']
    print("Logging in as " + username)

    connection.login(username, password)
    return connection

try:
    c = open_connection()
    print("Login succesful " + str(c))
    c.logout()
except imaplib.IMAP4.error:
    print("Authentication error")
