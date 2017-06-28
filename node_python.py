'''
Created on Jun 27, 2017

@author: b_bar
'''
# now send the dict off to somewhere by writing server code...

import socket

import json 

## use this function to make more readable output of nested data structures
def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def getJSON(data):
    obj = json.loads(data) # turns this into a dictionary
    print pretty(obj)
    return obj




## ok so above is being the client for Labview and below is the server for Node

def sendNumbers(msg):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "check"
    sock.bind(('', 6350))
    

    sock.listen(1)
    conn, addr = sock.accept()
    print 'Connected by', addr   
    # this will send one string of json data that comes from LabView :D
    try:
        data = conn.recv(1024)

        print "Client Says: ", data
        conn.sendall(msg)
  
    except socket.error:
        print "Error Occured."
    
    conn.close()

#sendNumbers(msg)

def loopSystem():
    
    # connect to the server
    HOST = "localhost"   # The local host
    PORT = 6340             # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
    s.connect((HOST, PORT))
    s.settimeout(2) #just make this shorter than I should be receiving, since if it times out we'll try again
    
    while(1):
        try: #getting the data from LV
            packet_size = s.recv(4)
            packet_size = int(packet_size.decode("utf-8"))
            
            data = s.recv(packet_size)
            data = data.decode("utf-8") #so now we have the data that we want
            getJSON(data)
            sendNumbers(data) # so right now it gets to here then it's stuck until you run the Node code again.... need connection to stay open
        
        except socket.timeout:
            print 'timeout'
            pass
        
        except socket.error:
            sock.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
            s.connect((HOST, PORT))
            s.settimeout(1)
            
        
    
loopSystem()        
