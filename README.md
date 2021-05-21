# Accio
This project is the implementation of a reliable UDP protocol with a file transfer layer above it. The file transfer protocol allows transferring filesof various types like gif, mp3, We used Selective Repeat Algorithm to ensure reliability. It is a better alternative to other approaches like Go-Back-N and Stop and wait, which involve unnecessary retransmissions and a significantly lowered bandwidth respectively.

The user interface of the application was implemented using Java.

The actual application and file transfer protocol is implemented in Python.

## Details of the Files

The source code for the application is in the folder 'src'

The javaapplication folder has 3 files, corresponding to 3 JFrames.
- Home.java : This is the home page of the application.
- Send.java : This is the UI enabling the user to send a file.
- Receive.java : This is the UI enabling the user to receive a file 

The whole implementation has 6 files.
- packet.py : This file has a class which represents the packet structure. 
- client.py : The file has the sender's code. 
- client_utils.py : The file has the funtions needed by the sender.
- server.py : The file has the reciever's side of the implementation.
- server_utils.py : Contains the functions needed by the receiver.
- file_transfer.py : This the application file, that will prompt you for inputs and run accordingly.

Note : file_transfer.py enables you to run the application on cmd line without user interface.

## Instructions to run the program

- Download the project into your PC.
- Navigate to the project folder.
- Open two instances of the terminal from this folder.
- Run the following command in both terminals : java -jar "./dist/JavaApplication.jar"

You will have two intances of the application, use one instance as a sender and the other instance as a receiver

### Case 1: Sending the file

You will be prompted for the following inputs
  - Receiver's (Server's) IP address : 127.0.0.1 (localhost)
  - Receiver's listening port : 12345 (example)
  - File to be sent : file.txt (example, browse it from a folder)
  - Window size : 4 (example)
  - Sender's (Client's) port : 23621 (This should be > Reciever's IP + 10, if running on the same system)

### Case 2: Receiving the file

You will be prompted for the following inputs 
  - Receiver's (Server's) IP address : 127.0.0.1 (example)
  - Receiver's (Server's) port : 12345 (example)

#### The transfered files are saved in the directory 'accio'

Note:
- If you want to simulate the packet loss, uncomment the section in the file server.py which has random.random(). The value represents the probability of packet loss.
- First click on the receive button, so that the server starts listening.
- Then click on the send button to send the file.
