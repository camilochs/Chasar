import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect("tcp://%s:%s" % ("104.131.190.21", 6667))
socket.setsockopt(zmq.SUBSCRIBE, b"Chasar-Client")

while True:
    channel, data_recv = socket.recv_multipart()

    ##Receive the information of all client nodes connected.
    data_json = json.loads(data_recv.decode())
    print(data_json)