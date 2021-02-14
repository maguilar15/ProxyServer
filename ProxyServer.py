from socket import *
from threading import Thread
from func import start_proxy_server
import sys

if __name__ == '__main__':
    try:
        if len(sys.argv) <= 1:
            print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
            sys.exit(2)
        # The proxy server is listening at 8888
        tcpSerSock = socket(AF_INET, SOCK_STREAM)
        tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        tcpSerSock.bind((sys.argv[1], 8888))
        tcpSerSock.listen(100)
        while 1:
            t = Thread(name="CacheService",target=start_proxy_server, args=(tcpSerSock,),daemon=True)
            t.start()
            t.join()
    except SyntaxError:
        print(f"This script requires python 3.\nYour current python is {sys.version_info.major}.")
        sys.exit(2)