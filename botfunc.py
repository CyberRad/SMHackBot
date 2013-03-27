import socket,urllib,time,os,string,random
from xml.dom import minidom


def send(ssl_socket,text):
	if text.strip()!="":
            ssl_socket.write('PRIVMSG #SMHack :\001ACTION '+str(text).strip()+'\001\r\n')


def tweet(data):
        data=urllib.urlopen('https://twitter.com/statuses/user_timeline/327895148.rss?count=1').read()
        data=data.replace('\n',' ')
        data= data[data.find('<item>')+18:]
        return "Last Tweet: "+data[0:data.find('</title>')]

def site(data):
        data=urllib.urlopen('http://www.smhack.org/?feed=rss2').read()
        data=data[data.find('<item>')+16:]
        title=data[0:data.find("</title>")]
        data=data[data.find('<link>')+6:]
        data=data[0:data.find("</link>")]
        return 'Last Post: '+title+" - "+data

def help(data):
        data=data.replace('!','')
        helps={
                'tweet':'!tweet returns the latest tweet on the @SMHack1 twitter account.',
                'site':'!site returns the latest blog post on http://smhack.org/',
                'weather':'!weather returns the weather conditions outside the space.',
                'address':address(None),
                'request':'!request is used to make improvment or feature requests for SMHackBot.'
                }
        return helps[data] if data in helps else 'Available commands are: !'+' !'.join(helps.keys())

def weather(data):
	usock = urllib.urlopen('http://www.google.com/ig/api?weather=20639')
	xmldoc = minidom.parse(usock)
	usock.close()
	data=xmldoc.getElementsByTagName('current_conditions')[0].getElementsByTagName('condition')[0].getAttribute('data').strip() + ' - '
	data+="Temp: "+xmldoc.getElementsByTagName('current_conditions')[0].getElementsByTagName('temp_f')[0].getAttribute('data').strip() + ' - '
	data+=xmldoc.getElementsByTagName('current_conditions')[0].getElementsByTagName('humidity')[0].getAttribute('data').strip() + ' - '
	data+=xmldoc.getElementsByTagName('current_conditions')[0].getElementsByTagName('wind_condition')[0].getAttribute('data').strip()
	return data

def request(data):
	if data != "":
	        f=open('requests.txt','a')
	        f.write(data+"\n\n")
	        f.close()
	        return "Thank you for the feature request."
	else:
		return "Use this command with text to request new features."


def address(data):
	return "2545 Solomons Island Rd, Apt. B, Huntingtown, MD 20639"

def chuck(data):
    filename="chuck"
    file=open(filename,'r')
    file_size=os.stat(filename)[6]
    file.seek((file.tell()+random.randint(0,file_size-1))%file_size)
    file.readline()
    line=file.readline()
    return line


def update(data):
        reload(botfunc)

commands={'tweet':tweet,'site':site,'address':address,'chuck':chuck,'weather':weather,'request':request,'help':help,'blog':site,'commands':help,'twit':tweet,'twat':tweet}

responder_commands={'tweet':tweet,'site':site,'weather':weather,'address':address,'chuck':chuck}