import socket
import select

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 6740))
server.listen()
server.setblocking(False)

print("Server is listening on port 6740...")

store = {}
sockets = [server]
buffers = {}

def accept(server):
    client,addr = server.accept()
    client.setblocking(False)
    sockets.append(client)
    buffers[client] = b""
    print(f"Connection established with {addr}")
    

def read(client):
    data = client.recv(1024)
    if not data:
        print("Client disconnected.")
        sockets.remove(client)
        buffers.pop(client,None)
        client.close()
        return

    buffers[client] += data
    while b"\n" in buffers[client]:
        line, buffers[client] = buffers[client].split(b"\n", 1)
        process_command(client, line)

def process_command(client, line):    
    command = line.decode().strip()
    parts = command.split(" ", 2)
    cmd = parts[0].upper()
    if cmd == "PING":
        response = "PONG\n"
    elif cmd == "SET":
        if len(parts)<3:
            response = "ERROR: SET command requires key and value\n"
        else:
            key,value = parts[1],parts[2]
            store[key] = value
            response = "OK\n"
    elif cmd == "GET":
        if len(parts)!=2:
            response = "ERROR: Wrong number of arguments for GET command\n"
        else:
            key = parts[1]
            if key in store:
                response = f"{store[key]}\n"
            else:
                response = "NULL\n"
    else:
        response = "UNKNOWN COMMAND\n"
    client.sendall(response.encode())

while True:
    readable,_,_ = select.select(sockets,[],[])
    for sock in readable:
        if sock == server:
            accept(server)
        else:
            read(sock)



        