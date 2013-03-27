#!/usr/bin/env python
import socket,urllib,sys,threading,time,botfunc

class pipein(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        threading.Thread.daemon = True

    def run (self):
      global irc
      while True:
         tmp=sys.stdin.readline().strip()
         if tmp !=  "":
            if tmp == "update":
                reload(botfunc)
            else:
                irc.send('PRIVMSG #SMHack :\001ACTION '+tmp.strip()+'\001\r\n')
            print tmp.strip()
         time.sleep(1)


while True:
    try:
        network = 'irc.freenode.net'

        port=7000
        irc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        irc.connect((network,port))

        ssl_socket = socket.ssl(irc)

        print repr(ssl_socket.server())
        print repr(ssl_socket.issuer())
        
        ssl_socket.write('NICK SMHackBot\r\n')
        ssl_socket.write('USER SMHackBot SMHackBot SMHackBot :SMHack Bot\r\n')
        ssl_socket.write('VERSION 1\r\n')
        ssl_socket.write('JOIN #SMHack\r\n')

        pipein().start()

        while True:
            data=ssl_socket.read()
            print data
            if data.find('PING')!=-1:
                print "Ping"
                ssl_socket.write('PONG '+data.split()[1]+'\r\n')
            #elif data.find('JOIN #SMHack')!=-1:
                #print "Join"
                #botfunc.send(ssl_socket,botfunc.site(data.strip()))
                #botfunc.send(ssl_socket,botfunc.tweet(data.strip()))
                #botfunc.send(ssl_socket,'Don\'t forget to Donate http://www.smhack.org/?page_id=67')
            #elif data.find('JOIN :#SMHack')!=-1:
                #print "Join"
                #botfunc.send(ssl_socket,botfunc.site(data.strip()))
                #botfunc.send(ssl_socket,botfunc.tweet(data.strip()))
                #botfunc.send(ssl_socket,'Don\'t forget to Donate http://www.smhack.org/?page_id=67')
            #elif data.find('MODE #SMHack +o')!=-1:
                #print "OP"
                #opname=data[data.find('MODE #SMHack +o ')+16:].strip()
                #print opname
                #botfunc.send(ssl_socket,'Welcome Channel Operator '+opname)
            elif data.find('TOPIC #SMHack :')!=-1:
                print "Topic"
                topic=data[data.find('TOPIC #SMHack :')+15:].strip()
                botfunc.send(ssl_socket,'New Channel Topic: '+topic)
            elif data.find('PRIVMSG #SMHack :!')!=-1:
                print "!found"
                data=data[data.find(' :!')+3:].strip()
                command,u,data=data.partition(" ")
                if command in botfunc.commands:
                    print command
                    botfunc.send(ssl_socket,botfunc.commands[command](data.strip()))

    except:
        print "You fat fingered something"
    time.sleep(30)
