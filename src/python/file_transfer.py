import os

print("Please select the mode in which you want to operate")
print("S : Sender")
print("R : Receiver")
op_mode = input("Please enter [S/R] : ")
if(op_mode=="S" or op_mode=="s"):
    os.system("python3 client.py")
elif(op_mode=="R" or op_mode=="r"):
    os.system("python3 server.py")
else:
    print("Invalid option.")
    print("Terminating the program")
    print("Thank you")