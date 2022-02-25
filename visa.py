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

def receberContrAtividade():
    while True:
        ctx = zmq.Context()
        sock = ctx.socket(zmq.SUB)
        sock.connect(f"tcp://{IP_ADDRESS}:5501")
    
        TOPIC = 'subProcesso'
        sock.subscribe(f"{TOPIC}")
        msg_string = sock.recv_string()
        msg_json = sock.recv_json()
        print(msg_json)
        data = msg_json
        data_converted = json.loads(data)
        codigo = data_converted['codigo']
        emaill = data_converted['emaill']
        status = data_converted['status']
        intencodigo = data_converted['itencodigo']
        nometitu = data_converted['nometitu']
        codcart = data_converted['codcart']
        bandeira = data_converted['bandeira']
        if(bandeira == 'visa'):
            if codcart == '10' :
                status = 'Compra_Efetuada_Com_Sucesso!'
            else:
                status = 'Erro_Ao_Validar_O_Cartao'
            msg= {}
            msg ['codigo'] = 11
            msg ['emaill'] = emaill
            msg ['status'] = status
            msg ['itencodigo'] = intencodigo
            msg ['nometitu'] = nometitu
            msg ['codcart'] = codcart
            msg ['bandeira'] = bandeira
            msg_json = json.dumps(msg)
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
        if(codigo == 11):
            msg_json = data
            TOPIC = 'confirmad'       
            sock.send_string(f"{TOPIC}", flags=zmq.SNDMORE)
            sock.send_json(msg_json) 
            codigo = 5

def main():
    pass
    _thread.start_new_thread(receberContrAtividade,())
    _thread.start_new_thread(enviar,())
    while True:
        pass

if __name__ == "__main__":
    main()