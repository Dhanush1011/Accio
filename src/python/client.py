import socket
import json
import threading
import signal
import time
import os
import packet
from client_utils import *
import sys

server_IP = sys.argv[1]
server_port = int(sys.argv[2])
window = int(sys.argv[3])
client_send_port = int(sys.argv[4])
input_file_path = sys.argv[5]
# input_file_path = input_file_path.replace("\\ "," ")
input_file_name = sys.argv[6]

# /print(server_IP, " ", server_port, " ", window, " ", client_send_port, " ", input_file_path, " ", input_file_name)

client_ack_port = client_send_port + 5
server_address = (server_IP,server_port)

client_send_soket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_send_soket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_send_soket.bind(('', client_send_port))

client_ack_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_ack_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_ack_socket.bind(('', client_ack_port))

packet_list = make_packets(input_file_path, input_file_name, 128)
max_pkt_no = len(packet_list)
pkt_head = -1
ack_recvd = -1
ack_expected = 0
lock = threading.Lock()
ack_buffer = []
flag = 0

# print("Client Started")
# start_time = time.time()

def reset_head(signum, _):
    # print("**** Time Out ****")
    global pkt_head, ack_recvd, ack_expected
    if(ack_recvd<max_pkt_no-1):
        pkt_head = ack_recvd
    signal.setitimer(signal.ITIMER_REAL, 0.7)

def send():
    global pkt_head, ack_recvd, ack_expected, flag
    while int(ack_recvd) < max_pkt_no - 1:
        if(flag==1):
            break
        with lock:
            while pkt_head - int(ack_recvd) < window:
                pkt_head = pkt_head + 1
                if pkt_head > max_pkt_no - 1:
                    break
                sending_packet = packet_list[pkt_head]
                if (sending_packet['status'] == False):
                    # print("sending : ", sending_packet['number'])
                    sending_data = json.dumps(sending_packet).encode('utf-8')
                    client_send_soket.sendto(sending_data, server_address)
        continue

class Ack(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.ack_socket = socket
        #print("Ack Thread created")

    def run(self):
        #print("Ack Thread started")
        global pkt_head, flag, ack_recvd, ack_expected, ack_buffer
        while True:
            if(check_file_end(ack_recvd,max_pkt_no,ack_buffer)):
                return

            data, from_address = self.ack_socket.recvfrom(1024)
            data = json.loads(data.decode('utf-8'))

            # if(check_close_ack(ack_recvd,max_pkt_no,data)):
            #     return

            if(check_ack(data)):
                if(data['pkt_type']=="close_ack"):
                    # print("Hi")
                    flag = 1
                    return

                with lock:
                    ack_number = int(data['number'])
                    if(ack_number==ack_expected):
                        # print("Recieved ack : ",ack_number)
                        ack_recvd = ack_number
                        ack_expected = ack_expected + 1
                        packet_list[ack_number]['status'] = True
                        signal.setitimer(signal.ITIMER_REAL, 0.7)
                        # print(ack_buffer)
                        while len(ack_buffer)!=0 and ack_buffer[0]==ack_expected:
                            ack_recvd = ack_buffer[0]
                            ack_expected = ack_expected + 1
                            ack_buffer.remove(ack_buffer[0]);
                            # print(ack_buffer)
                            ack_buffer.sort()

                    elif(ack_number>ack_expected):
                        # print("Recieved an ack out of the sequence : ", ack_number)
                        if ack_number not in ack_buffer:
                            ack_buffer.append(ack_number)
                            ack_buffer.sort()
                            packet_list[ack_number]['status'] = True

ack_thread = Ack(client_ack_socket)
ack_thread.start()

signal.signal(signal.SIGALRM, reset_head)
signal.setitimer(signal.ITIMER_REAL, 0.7)

send()
ack_thread.join()

print(1)


# print(input_file_name + " File Sent!")
# print("Thank you....")
# end_time = time.time()
# duration = end_time-start_time
# print(duration)
# file_size = os.path.getsize(input_file)
# print(file_size)
