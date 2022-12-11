import sys
import os
import sqlite3
import time
import datetime
from sqlite3 import Error


# CLASSES

class currentUser:
    def __init__(self, userID, fname, lname, username):
        self.userID = userID
        self.fname = fname
        self.lname = lname
        self.username = username

        self.isRegistered = False
        self.loggedIn = False
        self.emails = []
        self.owner = False

def create_connection():
    connection = None
    try:
       connection = sqlite3.connect("database\LookInnaBook.sql")

    except Error as e:
        print(f"[ERROR] '{e}'")

    return connection

def create_connection_from_dc():
    print("here")
    connection = None
    try:
        print(f"{os.path.dirname(os.getcwd())}\database\LookInnaBook.sql")
        connection = sqlite3.connect(f"{os.path.dirname(os.getcwd())}\LookInnaBook\database\LookInnaBook.sql")
        time.sleep(2)
    except Error as e:

        print(f"[ERROR] '{e}' (Directory: {os.path.dirname(os.getcwd())}\LookInnaBook\database\LookInnaBook.sql")
        time.sleep(2)

    return connection

def executeSQLFromFile(filename, connection):
    c = connection.cursor()

    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        try:
            c.execute(command)
            connection.commit()
        except Error as e:
            print(f"[ERROR] '{e}'")

def executeSQLFromLocal(query, connection):
    #print(f"QUERY: {query}")
    #time.sleep(2)

    c = connection.cursor()
    result = None

    try:
        c.execute(query)
        connection.commit()

        result = c.fetchall()
        return result
    except Error as e:
        print(f"[ERROR] '{e}'")
    
    time.sleep(2)
