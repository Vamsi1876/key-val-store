import socket

sock = socket.socket()
sock.bind(("0.0.0.0",6740))
sock.listen()
print("Server is listening on port 6740...")

client_sock,addr = sock.accept()
print(f"Connection established with {addr}")
store = {}
while True:
    data = client_sock.recv(1024)
    if not data:
        print("Client disconnected.")
        break
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
    print(store)
    client_sock.sendall(response.encode())
client_sock.close()
sock.close()