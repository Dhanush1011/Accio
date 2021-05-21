import hashlib

def checksum(data,pkt_type,number,status):
    hash_str = str(data) + ":" + pkt_type + ":" + str(number) + ":" + str(status)
    return hashlib.md5(hash_str.encode()).hexdigest()

class data_packet:

    def __init__(self, data, pkt_type, number, status):
        self.data = data
        self.pkt_type = pkt_type
        self.number = number
        self.status = status
        self.checksum = checksum(data,pkt_type,number,status)

    def make_dictionary(self):
        dict = {
            "data": list(self.data),
            "pkt_type": self.pkt_type,
            "number": self.number,
            "status": self.status,
            "checksum": self.checksum
        }
        return dict