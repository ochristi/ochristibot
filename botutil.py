import re                       # regex
import urllib.request           # read urls
from xml.dom import minidom     # parse xml

def checkuser(l):
    return re.match(r":ochristi!~ochristi@p5790336A.dip.t-dialin.net", str(l))

def listen(send, data):
    #if checkuser()
    #print(">>> checking for command")
    #print(data[3])
    rest = " ".join(data[4:])
    if data[3] == ":Ωjoin":
        #print(data[3])
        send("JOIN %s\r\n" % data[4])
    elif data[3] == ":Ωsay":
        #print(data[3])
        send("PRIVMSG %s :%s \r\n" % (data[2], rest))
    elif data[3] == ":Æehw":
        #print(data[3])
        send("PRIVMSG %s :ehw the Ω, do you like Æ better? \r\n" % data[2])
    elif re.match(r":[^ ]*youtube\.com.*", data[3]):
        send("PRIVMSG %s :%s\r\n" % (data[2], getYT(data[3])))

def getYT(url):
    base = "https://gdata.youtube.com/feeds/api/videos/"
    #v = "amYzBQMT4VI"
    #url = "http://www.youtube.com/watch?v=WnzlbyTZsQY&list=blah"
    v = re.match(r"(.+\.)*(youtube\.com).*[?&]v=([^&]+).*", url).group(3)
    try:
        response = urllib.request.urlopen(base+v).read()
    except:
        pass
    #myxml = minidom.parse(response)
    myxml = minidom.parseString(response)
    title = myxml.getElementsByTagName("title")[0].firstChild.toxml()
    #rating = myxml.getElementsByTagName("gd:rating")[0].firstChild.toxml()
    rating = "%.2f" % float(myxml.getElementsByTagName("gd:rating")[0].getAttribute("average"))
    return "%s - %s/5" % (title, rating)

def test():
    print("Hello World!")
