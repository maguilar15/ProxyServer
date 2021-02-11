import os, requests

def start_proxy_server(tcpServerSocket):
    print('Ready to serve...')
    ## FILL IN HERE...
    tcpCliSock, addr = tcpServerSocket.accept()

    print('Received a connection from:', addr)

    message = tcpCliSock.recv(1024)
    print(message)
    # Extract the filename from the given message
    filename = message.decode("utf-8").split("/")[1]
    filename = filename.replace("HTTP", "")  # result: www.yahoo.com
    print(f"Searching for: {filename}")
    filetouse = filename.strip()
    ## FILL IN HERE...
    fileExist = "false"
    try:
        if not os.path.exists(os.path.join(os.getcwd(), filename)):
            print(f"File does not exist in cache, searching for filename={filename}")
            fileExist = "false"
            raise IOError

        #fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode("utf-8"))
        tcpCliSock.send("Content-Type:text/html; charset=UTF-8\r\n".encode("utf-8"))
        tcpCliSock.send("Connection: close\r\n".encode("utf-8"))

        ## FILL IN HERE...
        print(f"{filename} is stored in cache.")
        obj = open(filename,"r", encoding="utf8", errors='ignore').readlines()
        print(f"Loading the web page {filename} with {len(obj)} number of bytes.")
        [tcpCliSock.send(e.encode("utf-8")) for e in obj]
    # Error handling for file not found in cache, need to talk to origin server and get the file
    except IOError:
        if fileExist == "false":
            ## FILL IN HERE...
            hostname = filename.replace("www.","").strip()
            requestData = f"GET / HTTP/1.1\r\nHost: {filename}\r\nConnection: keep-alive\r\n\r\n"
            try:
                print(f"Fetching from Origin Server.........................Request Data\n{requestData}")
                r = requests.get(f"https://{filetouse}",headers=None,stream=True)
                print(f"Response Code: {r} for {filename}")
                with open(filename,"wb") as f:
                    f.write(r.content)
                    tcpCliSock.send(r.content)
                    f.close()
                print(f"written {filename} to cache.")
            except Exception as e:
                print(f"Illegal request, exception={e}")
                # HTTP response message for file not found
                tcpCliSock.send("HTTP/1.0 404 sendErrorErrorError\r\n".encode("utf-8"))
                tcpCliSock.send("Content-Type:text/html\r\n".encode("utf-8"))
                tcpCliSock.send("\r\n".encode("utf-8"))
    tcpCliSock.close()