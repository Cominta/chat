import socket
import threading

HOST = "192.168.64.106"
PORT = 11719
clients = []

global clientsADDR
global clientsNick
clientsADDR = {}
clientsNick = []

def CreateServer(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind(("0.0.0.0", port))
    sock.listen()

    return sock

def Accepter(sock, cid, clients):
    global clientAddr
    clientSock, clientAddr = sock.accept()
    clients.append(clientSock)

    for i in range(len(clientsNick)):
        message = f"INF NICKS {len(clientsNick)} " + clientsNick[i]
        clientSock.send(message.encode("utf-8"))

    print(f"Client #{cid} connected " + f"({clientAddr[0]} {clientAddr[1]})")

    return clientSock

def ReadRequest(clientSock, cid):
    request = bytearray()

    try:
        while True:
            chunk = clientSock.recv(1024)

            if not chunk:
                return None

            request = chunk
            #print(request.decode("utf-8"))
            return request

    except ConnectionResetError:
        return None

    except:
        raise ConnectionResetError

def WriteResponse(sock, clients, request, clientSock, cid, clientsADDR):
    i = 0
    for i in range(len(clients)):
        try:
            clients[i].send(request)

        except ConnectionResetError:
            pass

        except ConnectionAbortedError:
            raise ConnectionResetError

    HandleClient(clients, sock, clientSock, cid, clientAddr)

def HandleClient(clients, sock, clientSock, cid, clientAddr):
    request = None
    request = ReadRequest(clientSock, cid)

    if request is None:
        cid -= 1
        print(f"Client #{cid} unexpectedly disconnected")

        ip = clientSock.getpeername()[0]
        alias = clientsADDR[ip]
        clientsNick.remove(alias)
        clientsADDR.pop(ip)
        clients.remove(clientSock)

        for i in range(len(clients)):
            clients[i].send(("INF NICKDEL " + alias).encode("utf-8"))

        return

    elif "INF" in request.decode("utf-8"):
        #print(request)
        requestINF = request.decode("utf-8").split()

        if requestINF[1] == "IPP":
            requestIPP = requestINF[2]
            clientsADDR[requestIPP] = requestINF[3]
            clientsNick.append(requestINF[3])
            #print(clientsADDR)

        elif requestINF[1] == "ALICHANG":
            aliasPersOld = requestINF[2]
            aliasPersNew = requestINF[3]
            ip = requestINF[4]

            clientsNick.remove(aliasPersOld)
            clientsNick.append(aliasPersNew)
            clientsADDR[ip] = aliasPersNew

        HandleClient(clients, sock, clientSock, cid, clientAddr)

    else:
        WriteResponse(sock, clients, request, clientSock, cid, clientsADDR)

def RunServer(port):
    sock = CreateServer(port)

    print("Server start")
    cid = 0

    while True:
        clientSock = Accepter(sock, cid, clients)
        cid += 1

        t1 = threading.Thread(target = HandleClient, args = ((clients, sock, clientSock, cid, clientAddr)))
        t1.start()

RunServer(PORT)