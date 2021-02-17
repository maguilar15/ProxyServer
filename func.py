from socket import *
import os, requests

def start_proxy_server(tcpServerSocket):
    print('Ready to serve...')
    ## FILL IN HERE...
    tcpCliSock, addr = tcpServerSocket.accept()

    print('Received a connection from:', addr)
    try:
        message = tcpCliSock.recv(1024)
        print(message.decode("utf-8"))
        filename = message.decode("utf-8").split("/")[1]
    except IndexError:
        print("empty message")
    ## FILL IN HERE...
    filename = filename.replace("HTTP", "").replace("www.","")  # result: www.yahoo.com
    hostname = f"www.{filename}"
    print(f"Searching for: {filename}, with hostname: {hostname}")
    filetouse = hostname.strip()
    fileExist = "false"
    try:
        if not os.path.exists(os.path.join(os.getcwd(), filetouse)):
            print(f"File does not exist in cache, searching for filename={filetouse}")
            fileExist = "false"
            raise IOError

        #fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode("utf-8"))
        tcpCliSock.send("Content-Type:text/html; charset=UTF-8\r\n".encode("utf-8"))
        tcpCliSock.send("Connection: close\r\n".encode("utf-8"))

        ## FILL IN HERE...
        print(f"{filetouse} is stored in cache.")
        obj = open(filetouse,"r", encoding="utf8", errors='ignore').readlines()
        print(f"Loading the web page {filetouse} with {len(obj)} number of bytes.")
        [tcpCliSock.send(e.encode("utf-8")) for e in obj]
    # Error handling for file not found in cache, need to talk to origin server and get the file
    except IOError:
        if fileExist == "false":
            ## FILL IN HERE...

            requestData = f"GET / HTTP/1.1\r\nHost: {hostname}\r\nConnection: keep-alive\r\n\r\n"
            try:
                print(f"Fetching from Origin Server.................................Request Data\n")
                headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                           }
                r = requests.get(f"https://{filetouse}",headers=headers,stream=True)
                print(f"Response Code: {r.status_code} for {filetouse}")
                with open(filetouse,"wb") as f:
                    f.write(r.content)
                    f.close()
                print(f"written {filename} to cache.")
            except Exception as e:
                print(f"Illegal request, exception={e}")
                # HTTP response message for file not found
                tcpCliSock.send("HTTP/1.0 404 sendErrorErrorError\r\n".encode("utf-8"))
                tcpCliSock.send("Content-Type:text/html\r\n".encode("utf-8"))
                tcpCliSock.send("\r\n".encode("utf-8"))
    tcpCliSock.close()

def handle_post_request(message=bytes):
    # PARSE (Request Type, data)
    p = message.decode("utf-8").split("\r\n")
    p2 = p[0].strip().split(" ")[0].strip()
    print(f"Request Type: {p2}")
    print(f"POST DATA: {p[-1].strip()}")
    return p2