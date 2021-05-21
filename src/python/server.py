import socket
import json
import hashlib
import random
import time
import sys
from packet import *
from server_utils import *

server_IP = sys.argv[1]
server_port = int(sys.argv[2])
server_ack_port = server_port + 5
file_path = sys.argv[3]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', server_port))

server_ack_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_ack_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_ack_socket.bind(('', server_ack_port))

pkt_buffer = []
pkt_expected = 0
pkt_recvd = -1
pkt_list = []

# print("Server Started")

def receive():
    global pkt_list,pkt_recvd,pkt_expected,pkt_buffer
    while True:
        data, from_address = server_socket.recvfrom(1024)
        data = json.loads(data.decode('utf-8'))
        data['data'] = bytes(data['data'])
        client_address = (from_address[0], from_address[1] + 5)

        # r = random.random()
        # if (r <= 0.8):
        #     print("Packet Loss")
        #     continue

        flag = -1
        if (check_packet(data) == 1):
            if (data['number'] < pkt_expected):
                ack_data = "Sending an ack"
                ack_data = bytes(ack_data, 'utf-8')
                if (data['pkt_type'] != 'close_pkt'):
                    ack_pkt = data_packet(ack_data, 'ack', int(data['number']), True)
                    ack_pkt = ack_pkt.make_dictionary()
                    sending_ack = json.dumps(ack_pkt).encode('utf-8')
                    server_ack_socket.sendto(sending_ack, client_address)

            elif (data['number'] == pkt_expected):
                # print(data['number'])
                ack_data = "Sending an ack"
                ack_data = bytes(ack_data, 'utf-8')
                if (data['pkt_type'] != 'close_pkt'):
                    ack_pkt = data_packet(ack_data, 'ack', int(data['number']), True)
                    ack_pkt = ack_pkt.make_dictionary()
                    sending_ack = json.dumps(ack_pkt).encode('utf-8')
                    server_ack_socket.sendto(sending_ack, client_address)
                pkt_expected = pkt_expected + 1
                pkt_recvd = data['number']
                data['status'] = True
                pkt_list.append(data)

                while len(pkt_buffer) != 0 and pkt_buffer[0] == pkt_expected:
                    pkt_recvd = pkt_buffer[0]
                    pkt_expected = pkt_expected + 1
                    pkt_buffer.remove(pkt_buffer[0]);
                    pkt_buffer.sort()
            else:
                # print(data['number'])
                ack_data = "Sending an ack"
                ack_data = bytes(ack_data, 'utf-8')
                if (data['pkt_type'] != 'close_pkt'):
                    ack_pkt = data_packet(ack_data, 'ack', int(data['number']), True)
                    ack_pkt = ack_pkt.make_dictionary()
                    sending_ack = json.dumps(ack_pkt).encode('utf-8')
                    server_ack_socket.sendto(sending_ack, client_address)
                data['status'] = True
                if data['number'] not in pkt_buffer:
                    pkt_list.append(data)
                    pkt_buffer.append(data['number'])
                    pkt_buffer.sort()

            for i in pkt_list:
                if (i['number'] == pkt_recvd and i['pkt_type'] == "close_pkt"):
                    flag = pkt_recvd
                    # print("Hi")
                    for i in range(0, 100):
                        ack_data = "Sending an ack"
                        ack_data = bytes(ack_data, 'utf-8')
                        ack_pkt = data_packet(ack_data, 'close_ack', pkt_recvd, True)
                        ack_pkt = ack_pkt.make_dictionary()
                        sending_ack = json.dumps(ack_pkt).encode('utf-8')
                        server_ack_socket.sendto(sending_ack, client_address)
                    break

            if (flag != -1):
                break



receive()
final_data_list = sorted(pkt_list,key=lambda k: k['number'])
for i in final_data_list:
    if(i['pkt_type']=="file_pkt"):
        output_file = file_path + i['data'].decode('utf-8')
        break

fd = open(output_file, 'wb')
for i in final_data_list:
    if(i['pkt_type']=="data_pkt"):
        fd.write(i['data'])

print(1)

# print("File received and saved as : " + output_file)
# print("Thank you!")
