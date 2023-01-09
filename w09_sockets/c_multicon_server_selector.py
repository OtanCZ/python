# multiconn-server.py
# Možnosti pro vícenásobné spojení (více klientů) na server:
# 1. použití vláken
# 2. použití asyncio
# 3. použití třídy Selector z balíčku selectors. Její instance bude registrována
#    k danému socketu.

import sys
import socket
import selectors
import types

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        # data nedorazila, což znamená, že klient socket zavřel. Zavřeme ho tedy i na straně serveru
        else:
            print(f"Closing connection to {data.addr}")
            # odstranění z monitoringu selectů
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
       
sel = selectors.DefaultSelector()     
host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)
try:
    while True:
        #blokující operace, pro každý socket vrací danou n-tici
        events = sel.select(timeout=None)
        for key, mask in events:
            # je událost od naslouchajícího socketu?
            if key.data is None:
                accept_wrapper(key.fileobj)
            # socket již byl akceptován
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()