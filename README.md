

### A lightweight library health monitoring multi-platform for remote computer's .

Chasar library have two principal components:

MasterNode:

*   It's installed in one server.

ClientNode

*   It can be installed in N remote computer's.


Each client node send information in json format to master node. This data can be memory, cpu, disk usage and
network description that extracted itself.
The client node send information approximately each one second.


## Prerequisite

*   Python 3.0+
*   pip3

## Installation

```python
git clone https://github.com/camilochs/chasar.git
cd chasar
pip3 setup.py install

```

##Usage: Master node

First, must initialize the master node:

```js
chasar masternode start [ip-address-bind] [port]

```
Default:
[ip-address-bind] = 127.0.0.1
[port] = 5555

For example, If you want specify a ipadress or port:

```js
chasar masternode start 190.12.0.0 5554

```

##Usage: Client node

After installed chasar in you remote computer:

```js
chasar clientnode start [ip-address-the-masternode] [port]

```
Default:
[ip-address-the-masternode] = 127.0.0.1
[port] = 5555

So, If you master node was created with the next parameters:

```js
chasar masternode start 190.1.0.0 5554

```

You client node command must be:

```js
chasar clientnode start 190.1.0.0 5554

```
And ready! You client node begin to send information to master node.

###Client

Also, Chasar allow subscribe to Master node(with zeromq) for receiver the information from all client nodes.

**Note: All subscribers have the port 6666.**

#### Example(Python): Communication with Master node.

```python
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect("tcp://%s:%s" % ("104.131.190.21", 6666))
socket.setsockopt(zmq.SUBSCRIBE, b"Chasar-Client")

while True:
    channel, data_recv = socket.recv_multipart()

    ##Receive the information of all client nodes connected.
    data_json = json.loads(data_recv.decode())
    print(data_json)

```

#### Example(NodeJS): Communication with Master node.

**Note: Must have zmq binding(version nodejs) installed. Url: https://github.com/JustinTulloss/zeromq.node**

```js
var zeromq = require('zmq'),
    ipPort = 'tcp://104.131.190.21:6666',
    socket = zeromq.socket('sub');

socket.connect(ipPort);
socket.subscribe('Chasar-Client');

//Receive the information of all client nodes connected.
socket.on('message', function(channel, data) {
    var info = JSON.parse(data);
    console.log(info);
});

```

See example of data receive(json):
/example/data recieve/data.json


