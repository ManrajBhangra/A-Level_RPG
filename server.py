import json
import socket
import threading

HOST = "127.0.0.1"  # Creates host and port for server
PORT = 12789

client_list = []  # Creates variables needed later in code
playerNum = 1
end = False


def receive_message(conn, client_list, end):
    ##### receive_message #######
    # Parameters :- conn, client_list: list, end:boolean
    # Return Type :- none
    # Purpose :- Has server receive messages from clients and send them to the other client
    ###########################
    while True:  # Creates infinite loop
        try:
            data = conn.recv(1024)
            if not data:
                continue
            else:
                msg = json.loads(data.decode())
                if msg["Data"]["playerNum"] == 2:
                    otherClient = client_list[0]
                else:
                    otherClient = client_list[1]
                otherClient.sendall(json.dumps(msg).encode())

            if msg["Data"]["Move"] == "Close":
                end = True
                return end

        except:  # Stops server from crashing when clients disconnect
            end = True
            return end


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, PORT))  # Creates server
    s.listen(1)
    print("Server is created")

except:
    print("Unable to start up server")  # Error message if problem with host and port

while not end:

    conn, addr = s.accept()
    threading.Thread(target=receive_message, args=(conn, client_list, end)).start()  # Begins threading
    client_list.append(conn)
    playerNum += 1
    if len(client_list) < 2:  # Waits until Client list is full to receive new messages
        for client in client_list:
            msg = {"Command": "WAIT"}
            client.sendall(json.dumps(msg).encode())
    else:
        print("Both clients connected")
        for playerNum in range(len(client_list)):  # Tells client their playerNum
            client = client_list[playerNum]
            msg = {"Command": "SETUP", "Data": {"PlayerNum": playerNum + 1}}
            client.sendall(json.dumps(msg).encode())
        Both_Conn = True


