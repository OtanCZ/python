# multiconn-client.py

import sys
import socket
import selectors
import types

# deklarace selektoru umožňujícího vícenásobné spojení
sel = selectors.DefaultSelector()
# b před uvozovkami znmená, že každé písmenko bude mít 8bit. hodnotu
messages = [b"prvni zprava od klienta.", b"druha zprava od klienta."]

# inicializace spojení
def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print(f"Starting connection {connid} to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # každý socket nastaven do neblokujícího módu
        sock.setblocking(False)
        # rozdíl oproti connect(addr): connect(addr) může vyhodit výjimku BlockingIOError exception,
        # connect_ex(addr) pouze může vrátit indikátor chyby errno.EINPROGRESS
        sock.connect_ex(server_addr)
        # registrujeme události, kdy je socket připraven ke čtení, či zápisu dat
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        # efektivní způsob vytvoření datové struktury bez deklarace třídy
        data = types.SimpleNamespace(
            connid=connid,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            # hluboká kopie messages použite z důvodu možné změny dat.
            messages=messages.copy(),
            outb=b"",
        )
        # registrace selektoru
        sel.register(sock, events, data=data)
        
#key - an instance of SelectorKey class - a namedtuple used to associate a file object to its underlying file descriptor,
#      selected event mask and attached data. It is returned by several BaseSelector methods.
#      fileobj - File object registered (socket reference).
#      fd      - Underlying file descriptor.
#      events  - Events that must be waited for on this file object.
#      data    - Optional opaque data associated to this file object: for example,
#                this could be used to store a per-client session ID.        

# mask - informace, jak má být s daty nakládáno. Hodnoty např. v konstantách 
#        selectors.EVENT_READ, nebo selectors.EVENT_WRITE
def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            print(f"Received {recv_data!r} from connection {data.connid}")
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print(f"Closing connection {data.connid}")
            # odstranění z monitoringu selectů
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print(f"Sending {data.outb!r} to connection {data.connid}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <host> <port> <num_connections>")
    sys.exit(1)

host, port, num_conns = sys.argv[1:4]
start_connections(host, int(port), int(num_conns))

try:
    while True:
        events = sel.select(timeout=1)
        if events:
            for key, mask in events:
                service_connection(key, mask)
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()