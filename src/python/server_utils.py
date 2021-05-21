import hashlib

def checksum(data,pkt_type,number,status):
    hash_str = str(data) + ":" + pkt_type + ":" + str(number) + ":" + str(status)
    return hashlib.md5(hash_str.encode()).hexdigest()

def check_packet(pkt):
    if(checksum(pkt['data'],pkt['pkt_type'],pkt['number'],pkt['status'])==pkt['checksum']):
        return 1
    else:
        return 0