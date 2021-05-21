from packet import *

def make_packets(file_path, file_name, segment_size):
    packet_list = []
    pno = 0
    fd = open(file_path, 'rb')
    file = fd.read()

    while (len(file) != 0):
        data = file[0:segment_size]
        temp_packet = data_packet(data, "data_pkt", pno, False)
        temp_packet = temp_packet.make_dictionary()
        packet_list.append(temp_packet)
        pno = pno + 1
        file = file[segment_size:]

    data = file_name
    data = bytes(data,'utf-8')
    file_name_pkt = data_packet(data,"file_pkt",pno,False)
    file_name_pkt = file_name_pkt.make_dictionary()
    packet_list.append(file_name_pkt)
    pno = pno +1

    data = "All packets sent"
    data = bytes(data,'utf-8')
    last_packet = data_packet(data,"close_pkt",pno,False)
    last_packet = last_packet.make_dictionary()
    packet_list.append(last_packet)

    return packet_list

def check_file_end(ack_recvd, max_pkt_no, ack_buffer):
    if (ack_recvd == max_pkt_no - 1 and len(ack_buffer) == 0):
        print("Received the closing ack 1st condition\n")
        return True
    else:
        return False

def check_close_ack(ack_recvd, max_pkt_no, data):
    if (ack_recvd == max_pkt_no - 1 and data['pkt_type']=="close_ack"):
        print("Received the closing ack 2nd condition\n")
        return True
    else:
        return False

def checksum(data,pkt_type,number,status):
    hash_str = str(data) + ":" + pkt_type + ":" + str(number) + ":" + str(status)
    return hashlib.md5(hash_str.encode()).hexdigest()

def check_ack(ack):
    ack_data = bytes(ack['data'])
    if (checksum(ack_data, ack['pkt_type'], ack['number'], ack['status']) == ack['checksum']):
        return True
    else:
        return False