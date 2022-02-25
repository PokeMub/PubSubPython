import socket
import _thread
import json
import zmq
import sys
import os
import time

IP_ADDRESS = '10.0.1.1'
TOPIC = None
fila_msgs = []

def receberServi():
    while True:
        ctx = zmq.Context()
        sock = ctx.socket(zmq.SUB)
        sock.connect(f"tcp://{IP_ADDRESS}:5501")
    
        TOPIC = 'enviarcontrrr'
        sock.subscribe(f"{TOPIC}")
        msg_string = sock.recv_string()
        msg_json = sock.recv_json()
        print(msg_json)
        fila_msgs.append(msg_json) 

def enviar():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUB)
    sock.connect(f"tcp://{IP_ADDRESS}:5500")
    codigo = 5
    while True:
        if(len(fila_msgs) == 0):
            pass
        else:
            data = fila_msgs.pop(0)
            data_converted = json.loads(data)
            codigo = data_converted['codigo']

        if(codigo == 9):
            #enviar para o sub Processo
            msg_json = data
            TOPIC = 'subProcesso'       
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json) 
            codigo = 5
        if(codigo == 18):
            msg_json = data
            TOPIC = 'confirmadasooo'       
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json) 
            codigo = 5
            print("teste")
            #enviar para servidor
def receberSubProc():
    while True:
        ctx = zmq.Context()
        sock = ctx.socket(zmq.SUB)
        sock.connect(f"tcp://{IP_ADDRESS}:5501")
    
        TOPIC = 'confirmad'
        sock.subscribe(f"{TOPIC}")
        msg_string = sock.recv_string()
        msg_json = sock.recv_json()
        data = msg_json
        data_converted = json.loads(data)
        codigo = data_converted['codigo']
        emaill = data_converted['emaill']
        status = data_converted['status']
        intencodigo = data_converted['itencodigo']
        nometitu = data_converted['nometitu']
        codcart = data_converted['codcart']
        bandeira = data_converted['bandeira']
        msg= {}
        msg ['codigo'] = 18
        msg ['emaill'] = emaill
        msg ['status'] = status
        msg ['itencodigo'] = intencodigo
        msg ['nometitu'] = nometitu
        msg ['codcart'] = codcart
        msg ['bandeira'] = bandeira
        msg_json = json.dumps(msg)
        print(msg_json)
        fila_msgs.append(msg_json) 
    

def main():
    _thread.start_new_thread(receberServi,())
    _thread.start_new_thread(enviar,())
    _thread.start_new_thread(receberSubProc,())
    while True:
        pass

if __name__ == "__main__":
    main()