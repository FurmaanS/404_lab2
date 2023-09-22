import socket

BYTES_TO_READ = 4096

def get(host, port):
    request = b"GET / HTTP/1.1\nHost: www.google.com\n\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #initalize socket
    s.connect((host, port)) #establish connection
    s.send(request) #send the request
    s.shutdown(socket.SHUT_WR) #tell that your done sending request
    chunk = s.recv(BYTES_TO_READ)
    result = b'' + chunk

    while(len(chunk)>0):
        chunk = s.recv(BYTES_TO_READ)
        result += chunk

    s.close() #close socket
    return result

print(get("127.0.0.1", 8080))
