var zeromq = require('zmq'),
    ipPort = 'tcp://104.131.190.21:6667',
    socket = zeromq.socket('sub');

socket.connect(ipPort);
socket.subscribe('Chasar-Client');

//Receive the information of all client nodes connected.
socket.on('message', function(channel, data) {
    var info = JSON.parse(data);
    console.log(info);
});