import socket

BYTES_TO_READ = 4096

def get(host, port):
    request = b"GET / HTTP/1.1\nHost: " + host.encode('utf-8') + b"\n\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #initalize socket
    s.connect((host, port)) #establish connection
    s.send(request) #send the request
    s.shutdown(socket.SHUT_WR) #tell that your done sending request
    result = s.recv(BYTES_TO_READ) #keep recieving the response
    while(len(result)>0):
        print(result)
        result = s.recv(BYTES_TO_READ)

    s.close() #close socket

get("www.google.com", 80)
#get("localhost", 8080)
