import socket
from threading import Thread

BYTES_TO_READ = 4096
HOST = "127.0.0.1" #Localhost/loopback
PORT = 8080

def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(BYTES_TO_READ) #waiting for request to be recieved
            if not data: #emtpy data -> break
                break
            print(data)
            conn.sendall(data) #send to client

#single thread echo server
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #initalize socket
        s.bind((HOST, PORT)) #bind to host and port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #free up port and allow reuse
        s.listen() #listen for incoming connections
        conn, addr = s.accept() #conn is socet reffering to client, addr is address of client [ip, port]
        handle_connection(conn,addr) #send response

#multi thread echo server
def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.sock_STREAM) as s: #initalize socket
        s.bind((HOST, PORT)) #bind to host and port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allow reuse of port
        s.listen(2) #max 2 backlog of connections
        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()

start_server()
#start_threaded_server()
