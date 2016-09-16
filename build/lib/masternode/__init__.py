from __future__ import absolute_import
import zmq
import json
import signal
import sys
from . import applicationclient


def create_socket(port):
    """
    Create zmq sub socket.
    """
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    try:
        socket.bind("tcp://*:%s" % port)
    except zmq.error.ZMQError:
        print("Address already in use")
        sys.exit(1)

    socket.setsockopt(zmq.SUBSCRIBE, b"")
    print("Start node-masternode Subscribe")
    return socket, context


def handler_signal_keyboard(socket, context):
    """
    Manage control^z interruption and close socket.
    """
    def handler():
        socket.close()
        context.term()
    signal.signal(signal.SIGTSTP, handler)


def start(port=5555):
    """
    Begin to receive data from clients and create zmq pub socket by send data to clients.
    """
    socket, context = create_socket(port)
    handler_signal_keyboard(socket, context)

    app_client = applicationclient.ApplicationClient()
    data_pre_format = {}

    while True:
        try:
            channel, data_recv = socket.recv_multipart()
            data_json = json.loads(data_recv.decode())

            #data_pre_format[data_json["mac_address"]] = data_json
            app_client.send(json.dumps(data_json).encode())

        except (KeyboardInterrupt, SystemExit):

            socket.close()
            context.term()

