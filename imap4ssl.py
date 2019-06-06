import imaplib2 as imaplib
import configparser
import os

def open_connection(config):
    #Connect to server
    hostname = config['server']['hostname']
    port = config['server']['port']
    print ("Connecting to " + hostname)
    try:
        connection = imaplib.IMAP4_SSL(host=hostname)
    except:
        raise SystemExit("Couldn't connect to server.")
    print("Succesfully connected.")

    #Login to account
    username = config['account']['username']
    password = config['account']['password']
    print("Logging in as " + username)
    try:
        connection.login(username, password)
    except:
        raise SystemExit("Couldn't log in.")
    print("Logged in succesfully.")
    return connection
