
##Chasar
### A lightweight library health monitoring for remote computer's.

Chasar library have two principal components:

MasterNode:

*   It's installed in one server.

ClientNode

*   It can be installed in N remote computer's.


Each client node send information in json format to master node. This data can be memory, cpu, disk usage and
network description that extracted itself.
The client node send information approximately each one second.


## Installation

```python
git clone
pip3 setup.py install

```

##Usage: Master node

First, must initialize the master node:

```js
chasar masternode start [ip-address-bind] [port]

```
Default:
ip-address = 127.0.0.1
port = 5555

For example, If you want specify a ipadress or port:

```js
chasar masternode start 190.12.1.1 6666

```

##Usage: Client node

After installed chasar in you remote computer:

```js
chasar clientnode start [ip-address-the-masternode] [port]

```
Default:
ip-address-the-masternode = 127.0.0.1
port = 5555

So, If you master node was created with the next parameters:

```js
chasar masternode start 190.1.2.1 6666

```

You client node command must be:

```js
chasar clientnode start 190.1.2.1 6666

```


###Client

Also, Chasar allow subscribe to Master node(with zeromq) for receiver the information from the client nodes.


#### Example(Python): Communication with Master node.

```python
import pyzmq
import json

context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect("tcp://%s:%s" % ("127.0.0.1", 5555))
socket.setsockopt(zmq.SUBSCRIBE, b"Chasar-Client")

while True:
    channel, data_recv = socket.recv_multipart()

    ##Receive the information of all client nodes connected.
    data_json = json.loads(data_recv)
    pritn(data_json)

```

#### Example(NodeJS): Communication with Master node.

```js

var zeromq = require('zmq'),
    ipPort = 'tcp://127.0.0.1:5555',
    socket = zeromq.socket('sub');

socket.connect(ipPort);
socket.subscribe('Chasar-Client');

socket.on('message', function(channel, data) {
    console.log(data);
});

```
