import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080

#send data/request to host:port
def send_request(host, port, request):

    #with block closes socket once we are done
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        #connect socket to host:port
        client_socket.connect((host,port))
        #send request through connected socket
        client_socket.send(request)
        #shut socket to tell server we done sending data
        client_socket.shutdown(socket.SHUT_WR)

        #assemble the response here
        data = client_socket.recv(BYTES_TO_READ)
        result = b'' + data
        while len(data) > 0: #read until connection terminates
            data = client_socket.recv(BYTES_TO_READ)
            result += data

        #return the response
        return result

#handle incoming connection
def handle_connection(conn, addr):
    with conn:
        print(f"connected by {addr}")

        request = b''
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            request += data
            response = send_request("www.google.com", 80, request)
            conn.sendall(response)

#start single therad proxy server
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #initalize socket
        s.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT)) #bind to host and port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #free up port and allow reuse
        s.listen(2) #listen for incoming connections
        conn, addr = s.accept() #conn is socet reffering to client, addr is address of client [ip, port]
        handle_connection(conn,addr) #send response

#start multi thread server
def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(2)

        while True:
            conn, addr = s.accept()
            thread = Thread(target = handle_connection, args = (conn, addr))
            thread.run()

#start_server()
start_threaded_server()

