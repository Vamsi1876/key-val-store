import socket

sock = socket.socket()
sock.bind(("0.0.0.0",6740))
sock.listen()
print("Server is listening on port 6740...")

client_sock,addr = sock.accept()
print(f"Connection established with {addr}")

while True:
    data = client_sock.recv(1024)
    if not data:
        print("Client disconnected.")
        break
    client_sock.sendall(data)
client_sock.close()
sock.close()