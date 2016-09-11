import zmq


class ApplicationClient:
    """
    Class send data received in master node to application example.
    """
    def __init__(self, port=6666):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % port)
        self.socket.sndhwm = 1

    def send(self, data_json):
        print(data_json)
        self.socket.send_multipart([b"Chasar-Client", data_json])