# echo-server.py
# https://realpython.com/python-sockets/
# Blocking Calls
# A socket function or method that temporarily suspends your application is a blocking call. For example, .accept(), .connect(),
#  .send(), and .recv() block, meaning they don’t return immediately. Blocking calls have to wait on system calls (I/O) to complete
#  before they can return a value. So you, the caller, are blocked until they’re done or a timeout or other error occurs.
# Blocking socket calls can be set to non-blocking mode so they return immediately. If you do this, then you’ll need to at least
#  refactor or redesign your application to handle the socket operation when it’s ready.
# Because the call returns immediately, data may not be ready. The callee is waiting on the network and hasn’t had time to complete
#  its work. If this is the case, then the current status is the errno value socket.EWOULDBLOCK. Non-blocking mode is supported with 
# .setblocking().
# By default, sockets are always created in blocking mode. See Notes on socket timeouts for a description of the three modes.

# The byte ordering used in TCP/IP is big-endian and is referred to as network order.

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)