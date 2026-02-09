import socket
import select
import time

# ---------- Server Setup ----------
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 6740))
server.listen()
server.setblocking(False)

print("Server is listening on port 6740...")

store = {}          # key -> (value, expiry)
sockets = [server]
buffers = {}

# ---------- Helpers ----------
def is_expired(key):
    value, expiry = store[key]
    if expiry is None:
        return False
    if time.time() > expiry:
        del store[key]
        return True
    return False

# ---------- Command Handlers ----------
def handle_ping(_):
    return "PONG\n"


def handle_set(command):
    expiry = None
    cmd, key, rest = command.split(" ", 2)
    # Value MUST be quoted
    if not rest.startswith('"'):
        return "ERROR: Value must be enclosed in double quotes\n"

    # Find closing quote
    end = rest.find('"', 1)
    if end == -1:
        return "ERROR: Unterminated quote\n"

    value = rest[1:end]
    remainder = rest[end+1:].strip()

    # Optional EX ttl
    if remainder:
        parts = remainder.split()
        if len(parts) != 2 or parts[0].upper() != "EX":
            return "ERROR: Invalid SET syntax\n"

        try:
            ttl = int(parts[1])
            expiry = time.time() + ttl
        except ValueError:
            return "ERROR: TTL must be an integer\n"

    store[key] = (value, expiry)
    return "OK\n"

def handle_get(parts):
    if len(parts) != 2:
        return "ERROR: GET requires key\n"

    key = parts[1]
    if key not in store or is_expired(key):
        return "NULL\n"

    return f"{store[key][0]}\n"

def handle_del(parts):
    if len(parts) != 2:
        return "ERROR: DEL requires key\n"

    key = parts[1]
    if key in store:
        del store[key]
        return "OK\n"

    return "NULL\n"

def handle_exists(parts):
    if len(parts) != 2:
        return "ERROR: EXISTS requires key\n"

    key = parts[1]
    return "1\n" if key in store and not is_expired(key) else "0\n"

def handle_keys(_):
    keys = []
    for key in list(store.keys()):
        if not is_expired(key):
            keys.append(key)
    return " ".join(keys) + "\n"

def handle_flush(_):
    store.clear()
    return "OK\n"

def handle_ttl(parts):
    if len(parts) != 2:
        return "ERROR: TTL requires key\n"

    key = parts[1]
    if key not in store or is_expired(key):
        return "-Key does not exist\n"

    value, expiry = store[key]
    if expiry is None:
        return "No expiry\n"  # No expiry

    ttl = int(expiry - time.time())
    return f"{ttl}\n"

# ---------- Command Dispatcher ----------
COMMANDS = {
    "PING": handle_ping,
    "SET": handle_set,
    "GET": handle_get,
    "DEL": handle_del,
    "EXISTS": handle_exists,
    "KEYS": handle_keys,
    "FLUSH": handle_flush,
    "TTL": handle_ttl,
}

def process_command(command):
    parts = command.split()
    cmd = parts[0].upper()

    handler = COMMANDS.get(cmd)
    if not handler:
        return "UNKNOWN COMMAND\n"

    # SET needs full command string
    if cmd == "SET":
        return handler(command)

    return handler(parts)

# ---------- Networking ----------
def accept(server):
    client, addr = server.accept()
    client.setblocking(False)
    sockets.append(client)
    buffers[client] = b""
    print(f"Connection established with {addr}")

def read(client):
    data = client.recv(1024)
    if not data:
        sockets.remove(client)
        buffers.pop(client, None)
        client.close()
        return

    buffers[client] += data
    while b"\n" in buffers[client]:
        line, buffers[client] = buffers[client].split(b"\n", 1)
        response = process_command(line.decode().strip())
        client.sendall(response.encode())

# ---------- Event Loop ----------
while True:
    readable, _, _ = select.select(sockets, [], [])
    for sock in readable:
        if sock == server:
            accept(server)
        else:
            read(sock)
