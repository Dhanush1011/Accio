# Sender's Algorithm

We have two threads running Ack and main
- Ack thread listens to the ack's sent by the receiver
- Main thread sends the packet to the receiver
- We have 5 global variables shared commonly between both threads
    - ack_buffer	: Stores the ack values, incase if the ack are out of order 
    - ack_recvd		: Stores the latest correctly recvd ack
    - ack_expected	: The ack which we expect
    - packet_list	: This the initial packet list generated from the file
    - pkt_head		: Points to the last packet sent in the list
- In the main program, 
    - We first convert the file into packets and store them in a list.
    - We also append two more packets, one containing the name of the file, two containing the closing packet.
    - We call the send function.
    - We then loop until the ack_rcvd is greater than equal to the maximum packet number.
        - In the loop, we check if the distance between last packet sent and the last ack recvd is less than window size, then we send the increment the pkt_head.
        - If the packet's has been already sent successfully, we dont send it.
        - Else we send the packet.
- In the Ack thread, we receive the acks,
    - If the ack is received with no corruption, we proceed.
    - When the ack received is equal to the ack expected.
        - We increment the ack received and expected
        - We also update the status of the the packet, since it's received successfully.
        - We then check for the ack buffer, and see if we have some out of order acks
        - If we have and they are in order with what we expect, then we update the ack received and ack expected
    - When the ack received is greater than the ack expected, then that means it's out of order
        - We push it to the ack buffer
        - We update the status of the packet
- We also run the timer, with a value of 0.7 seconds.
    -When we reach a time out, we put the paket head to the start of the window.
    - As a result in, the main thread, the packet head will move across the window and send the files, whose acks haven't been received yet.

# Receiver's Algorithm

The receiver's role is to store the packets given by client and sending acknowledgements for the same
- We have 4 main variables
    - pkt_buffer	: Stores the packet's number, incase if the packets are out of order. 
    - pkt_recvd		: Stores the latest correctly recvd packet
    - pkt_expected	: The packet which we expect
    - packet_list	: This stores the packets received.
- We Verify that the packets sent remain uncorrupted by calculating the checksum of the packet comparing it with the checksum stored in the packet separately. 

- If the packet is not corrupted
    
    - If the packet received is less than packet expected, that means that we got the packet which was already received, and the ack sent is not received by the sender. That is why it sent the packet again.
        - So we just send the ack again.

    - If the packet received is equal to the packet expected,
        - We send the ack. 
        - We append the packet to the packet list 
        - We increment the packet received and packet expected. 
        - We remove packet values from the buffer if it's not empty and complies with the next sequence of expected packets.

    - If the packet received is greater than the packet expected
        - We send the ack
        - We append the packet to the packet list
        - We push this out of order packet to the packet buffer

- Finally, we sort the packet list.
- We search for the packet of the type "file_pkt". This has the file name in the data section.
- We then open the output file and write all the data from the packets of type "data_pkt"
- The "close_pkt" packet signals the end of transfer. 