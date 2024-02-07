import socket
import json

HOST = 'consumer'
PORT = 80

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print(f'Listening for connections on port {PORT}', flush=True)

while True:
    c, addr = s.accept()
    print(f'Connection received from {addr}\n')
    raw_msg = c.recv(1024).decode('utf-8')
    data = json.loads(raw_msg)
    print(f'Received data: {data}\n')
    summa = sum([x+1 for x in range(data['last_processed'], data['state_index'])])
    response_json = json.dumps({'status':'success', 'sum':summa, 'data':data})
    print(f'Sending response: {response_json}\n', flush=True)
    c.send(str.encode(response_json))
    c.close()
