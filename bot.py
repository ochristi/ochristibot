import sys
import imp
import socket
import string
from collections import deque
import re
import sqlite3
import botutil

class IRCBot:
    s = socket.socket()
    def __init__(self, config, papa):
        # settings import
        settings = __import__(config)
        self.HOST     = settings.HOST
        self.PORT     = settings.PORT
        self.NICK     = settings.NICK
        self.IDENT    = settings.IDENT
        self.REALNAME = settings.REALNAME
        self.papa     = papa
        # commands import
        #settings = __import__("botutil")
        # database
        self.db = sqlite3.connect('bot.sqlite')
        self.dbcursor = self.db.cursor()
        # initialize
        self.connect()
        self.run()
        self.exit()
    def connect(self):
        self.s.connect((self.HOST, self.PORT))
        self.updatestate(["%s:%s"%(self.HOST, self.PORT)])
        self.send("NICK %s\r\n" % self.NICK)
        self.send("USER %s %s bla :%s\r\n" % (self.IDENT, self.HOST, self.REALNAME))

        #self.send("QUIT %s\r\n" % "bye")
    def run(self):
        i = 0
        queue = deque()
        while 1:
            if len(queue) <= 1:
                #print("length low")
                incoming = self.s.recv(1024).decode('utf-8').split('\r\n')
                if len(queue) == 1:
                    incoming[0] = queue.popleft()+incoming[0]
                queue.extend(incoming)
            #print(incoming.decode('utf-8'))
            #rawstring = incoming.decode('utf-8').rstrip()
            #incoming.decode('utf-8').split('\r\n')
            rawstring = queue.popleft().rstrip()
            data = rawstring.split(" ")
            # log incoming data
            print (rawstring)
            self.log(rawstring)
            try:
                if (data[0] == "PING"):
                    self.send("PONG %s\r\n" % data[1])
                elif len(data) > 3 and data[3] == ":Ωquit":
                    print(">>> bot terminating...")
                    self.exit()
                    break
                elif len(data) > 3 and data[3] == ":Ωreload":
                    print(">>> bot reloading commands...")
                    imp.reload(botutil)
                    #break
                elif data[0] != ":"+self.HOST:
                    #print(">>> logging ...")
                    botutil.listen(self.send, data)
                    pass
            except:
                print ("Unexpected error:", sys.exc_info()[0])
                pass
            #incoming = self.s.recv(1024)
    def send(self, data):
        print ("<<< %s" % data)
        self.s.send(data.encode())
    def updatestate(self, server):
        self.dbcursor.execute("INSERT INTO botstate VALUES (NULL, ?, datetime('now'))", server)
        self.db.commit()
        self.dbcursor.execute("SELECT MAX(bsid) FROM botstate")
        self.bsid = self.dbcursor.fetchone()[0]
    def log(self, line):
        self.dbcursor.execute("INSERT INTO log VALUES (NULL, datetime('now'), ?, ?)", (line, self.bsid))
        self.db.commit()
    def exit(self):
        self.dbcursor.close()
        self.send("QUIT %s\r\n" % "bye")
        #self.s.close()

bot = IRCBot("freenode", "")

