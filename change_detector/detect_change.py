import json
import os.path
import time
import socket

SLICE_SIZE = 15

HOST = 'consumer'
PORT = 80

STATE_FILENAME = '/vol/state.json'
LOG_FILENAME = '/vol/log.json'

def check():
    state_index = read_state()
    last_processed = read_log()
    
    if state_index > last_processed:
        process_until = min(last_processed + SLICE_SIZE, state_index)
        success = process(last_processed, process_until)
        if success:
            log = json.dumps({'last_processed':process_until,'timestamp':time.time()})
            f = open(LOG_FILENAME, 'w+')
            f.write(log)
            f.close()
    else:
        print('Nothing to do this time.', flush=True)


def read_json_file(filename): 
    f = open(filename, 'r')
    data = json.load(f)
    f.close()
    return data


def read_log():
    last_processed = 0
    log_exists = os.path.isfile(LOG_FILENAME)
    if log_exists:
        log = read_json_file(LOG_FILENAME)
        print(f'read from log file: {log}', flush = True)
        last_processed = log['last_processed']
    return last_processed
    
    
def read_state():
    state = read_json_file(STATE_FILENAME)
    print(f'read from state file: {state}', flush = True)
    state_index = state['index']
    return state_index


def process(last_processed, process_until):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        json_string = json.dumps({'last_processed':last_processed,'state_index':process_until})
        s.send(str.encode(json_string))
        raw_msg = s.recv(1024).decode('utf-8')
        data = json.loads(raw_msg)
        if data['status'] == 'success':
            print(f'Succesfully processed, new log index: {data["data"]["state_index"]}', flush=True)
            return True
        else:
            print('Error while processing', flush=True)
            return False


while True:
    check()
    time.sleep(10)
