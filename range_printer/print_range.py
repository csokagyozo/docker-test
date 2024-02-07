import socket
import json

HOST = 'docker-test_range_printer_1'
PORT = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print(f'Listening for connections on port {PORT}', flush=True)

while True:
    c, addr = s.accept()
    print(f'Connection received from {addr}')
    raw_msg = c.recv(1024).decode('utf-8')
    data = json.loads(raw_msg)
    print(f'Received data: {data}')
    summa = sum([x+1 for x in range(data['from'], data['to'])])
    response_json = json.dumps({'status':'success', 'sum':summa, 'data':data})
    print(f'Sending response: {response_json}', flush=True)
    c.send(str.encode(response_json))
    c.close()
