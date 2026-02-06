import socket
import selectors

sel = selectors.DefaultSelector()
store = {}

def accept(server):
    client,addr = server.accept()
    client.setblocking(False)
    print(f"Connection established with {addr}")
    sel.register(client,selectors.EVENT_READ, read)

def read(client):
    data = client.recv(1024)
    if not data:
        print("Client disconnected.")
        sel.unregister(client)
        client.close()
        return

    command = data.decode().strip()
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
    

server = socket.socket()
server.bind(("0.0.0.0", 6740))
server.listen()
server.setblocking(False)

print("Server is listening on port 6740...")

sel.register(server,selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key,_ in events:
        callback = key.data
        callback(key.fileobj)



