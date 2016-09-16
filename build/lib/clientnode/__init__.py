
import zmq
import json
import psutil
import time
import datetime
import platform
import netifaces
import signal

def mac_address():
    """
    Return the mac address of computer.
    """
    interface = netifaces.ifaddresses('en0')
    info = interface[netifaces.AF_LINK]
    if info:
        return interface[netifaces.AF_LINK][0]["addr"]


def internet_addresses():
    """
    Return the info network.
    """
    interface = netifaces.ifaddresses('en0')
    info = interface[netifaces.AF_INET]
    if info:
        return interface[netifaces.AF_INET]


def pids_active(pids_computer):
    """
    This function find pids of computer and return the valid.
    """
    pid_valid = {}
    for pid in pids_computer:
        data = None
        try:
            process = psutil.Process(pid)
            data = {"pid": process.pid,
                    "status": process.status(),
                    "percent_cpu_used": process.cpu_percent(interval=0.0),
                    "percent_memory_used": process.memory_percent()}

        except (psutil.ZombieProcess, psutil.AccessDenied, psutil.NoSuchProcess):
            data = None

        if data is not None:
            pid_valid[process.name()] = data
    return pid_valid


def process_send_data(socket, context):
    """
    Send all memory, cpu, disk, network data of computer to server(master node)
    """
    while True:
        try:
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            memory_info = psutil.virtual_memory()
            disk_info = psutil.disk_usage('/')
            pids_computer = psutil.pids()

            info_to_send = json.dumps({
                "computer_utc_clock": str(datetime.datetime.utcnow()),
                "computer_clock": str(datetime.datetime.now()),
                "hostname": platform.node(),
                "mac_address": mac_address(),
                "ipv4_interfaces": internet_addresses(),
                "cpu": {
                    "percent_used": cpu_percent
                },
                "memory": {
                    "total_bytes": memory_info.total,
                    "total_bytes_used": memory_info.used,
                    "percent_used": memory_info.percent
                },
                "disk": {
                    "total_bytes": disk_info.total,
                    "total_bytes_used": disk_info.used,
                    "total_bytes_free": disk_info.free,
                    "percent_used": disk_info.percent
                },
                "process": pids_active(pids_computer)

            }).encode()
            #send json data in the channel 'status', although is not necessary to send.
            socket.send_multipart([b"status", info_to_send])
            #time.sleep(0.500)

        except (KeyboardInterrupt, SystemExit):
            socket.close()
            context.term()

def handler_signal_keyboard(socket, context):
    """
    Manage control^z interruption and close socket.
    """
    def handler():
        socket.close()
        context.term()
    signal.signal(signal.SIGTSTP, handler)


def start(ip_address='127.0.0.1', port=5555):
    """
    Connect to master node and each one second send data.
    """
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect("tcp://%s:%s" % (ip_address, port))
    socket.sndhwm = 1
    handler_signal_keyboard(socket, context)

    process_send_data(socket, context)
