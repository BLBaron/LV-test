// trying to bypass Python
// This code in it's current form will print out the data it is recieiving to the console window

var net = require('net');

var HOST = 'localhost';
var PORT = 6340; // port being used by LabVIew
var client = new net.Socket();

client.connect(PORT, HOST, function() {

    console.log('CONNECTED TO: ' + HOST + ':' + PORT);
    // Write a message to the socket as soon as the client is connected, the server will receive it as message from the client 
    client.write("hello");

});

// Add a 'data' event handler for the client socket
// data is what the server sent to this socket
client.on('data', function(data) {
    console.log('DATA: ' + data); //print recieved message to a console window
    
});

// Add a 'close' event handler for the client socket 
client.on('close', function() {
    console.log('Connection closed');
});

// add a 'error' event handler for the client socket
client.on('error', function() {
	console.log('there was an error');
});