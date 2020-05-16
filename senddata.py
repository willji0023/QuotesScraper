import socket, sys, requests, json
import errno, os

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
except:
    print("Socket failed with error %s") %(err)

port = 8080

try:
    host_ip = socket.gethostbyname('localhost')
except socket.gaierror: 
    print("There was an error resolving the host")
    sys.exit() 

s.connect((host_ip, port))
print("Connected to host") #on port == %s") %(host_ip) 

try:
    with open('GoodReadsData.json', 'r') as f: 
        if len(f) == null:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), 'GoodReadsData.json')
        data = json.load(f)
        payload = json.dumps(data).encode()
        s.sendall(payload)
except:
    print("Quotes not found")

