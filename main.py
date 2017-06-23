# 1. download and test labview file
# 2. initialize a socket object
# 3. socket.recieve -> give it a number of bytes that it will be getting. The LabView system will also send 4bytes of data indicating
# how long the rest of the message is. The message will probably come in a string? Unsure. But formatted like JSON. Or it'll just be a dict
# We will have to see how that works.
# 4. Parse and display the data sent from LabView
#     this means showing fields with the numbers generated, and updating them each time Labview sends new numbers
#     that'll be at the fastest once per second. Stop labview running just by closing the page? Might be better to have a button since that
#     will better reflect real use. We also want to test sending something back, which will be a number to change the send frequency
# when the client initializes connection via TCP that's when the generator starts running (or something)


## this is stuff for the web stuff
import webapp2
import jinja2
# this is stuff for processing. We might not need urllib
import urllib, urllib2, json

## this is stuff for debugging... I think
import os
import logging

## this is stuff for receiving and sending data via tcp
import socket
 
def getNums(): 
    HOST = "localhost"   # The local host
    PORT = 6340             # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
    s.connect((HOST, PORT))
    s.settimeout(5)
     
    packet_size = s.recv(4)
    packet_size = int(packet_size.decode("utf-8"))
    
    data = s.recv(packet_size)
    data = data.decode("utf-8") #so now we have the data that we want
    
    s.close()
    return data
#    print('Received', repr(data))
    

## and then from here is going to be code for processing that one string of data

import json 

## use this function to make more readable output of nested data structures
def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

## two lines below used for debugging
# print(data) #just doing this prints what looks like a dictionary (in string form)
# print type(data) # <- ok but apparently it's unicode and nor a string? 


def getJSON():
    data = getNums()
    obj = json.loads(data) # turns this into a dictionary
    print obj
    print type(obj)
    print pretty(obj)
    return obj


import threading

def f():
    getJSON()
    # call f() again in 5 seconds
    threading.Timer(5, f).start()

# start calling f now and every 60 sec thereafter


## for getting data up onto google app engine and connecting to the html file
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        obj = getJSON()
        template = JINJA_ENVIRONMENT.get_template('webtest.html')
        logging.info("In MainHandler")
        tval={}
        tval["numbers"] = obj
        logging.info(tval["numbers"])
        self.response.write(template.render(tval))


    
# for all URLs except alt.html, use MainHandler
application = webapp2.WSGIApplication([ \
                                      ('/.*', MainHandler)
                                      ],
                                     debug=True)

 