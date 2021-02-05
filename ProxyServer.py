#!/usr/bin/env python

from socket import *
import sys, os


try:
    if len(sys.argv) <= 1:
        print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
        sys.exit(2)
except SyntaxError:
    print("Use Python 3 to execute the Proxy Server.")


# The proxy server is listening at 8888
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(100)

print('Ready to serve...')

while 1:
    # Strat receiving data from the client
    tcpCliSock, addr = tcpSerSock.accept()

    print('Received a connection from:', addr)

    # Extract the filename from the given message
    message = tcpCliSock.recv(4096)
    print(message.decode("utf-8"))

    if message is None:
        raise Exception("Proxy Server has an empty response.")
    else:
        filename = message.decode("utf-8").split("/")[1]
        filename = filename.replace("HTTP", "")  # result: www.yahoo.com
        fileExist = "true"

    try:
        # Check whether the file exist in the cache
        cacheHit = os.path.exists(os.path.join(os.getcwd(), filename))
        print(f"Cache Hit: {cacheHit}")
        if not cacheHit:
            print(f"File does not exist in the proxy's cache: filename={filename}")
            fileExist = "false"
            raise IOError

        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode("utf-8"))
        tcpCliSock.send("Content-Type:text/html\r\n".encode("utf-8"))
        ## FILL IN HERE...
        #filetouse = open(filename, "r")
        print(f"File exists in proxy's cache: filename={filename}")

    # Error handling for file not found in cache, need to talk to origin server and get the file
    except IOError:

        if fileExist == "false":
            hostname = filename.replace("www.", "")  # result: yahoo.com
            print(f"Name or service not known and fetching: hostname={hostname}, filename={filename}")

            s = socket(AF_INET, SOCK_STREAM)
            s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            s.connect((hostname,80))

            requestData = f"GET http://{filename} HTTP/1.0\r\n\n"
            s.send(requestData.encode("utf-8"))
            data = s.recv(1024)
            print(f"Result: {repr(data)}")
            s.close()
    else:
        # HTTP response message for file not found
        tcpCliSock.send("HTTP/1.0 404 sendErrorErrorError\r\n".encode("utf-8"))
        tcpCliSock.send("Content-Type:text/html\r\n".encode("utf-8"))
        tcpCliSock.send("\r\n".encode("utf-8"))

# Close the client and the server sockets
    tcpCliSock.close()
    tcpSerSock.close()
