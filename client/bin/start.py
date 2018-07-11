import socket
from server.conf import setting
from client.core import src



if __name__ == '__main__':
    soc = socket.socket()
    soc.connect((setting.IP, setting.prot))
    while True:
        cmd = input('<>>>>>>>>>>>')
        if len(cmd) == 0:
            continue
        soc.send(cmd.encode('utf-8'))
        if hasattr(src.cliect,cmd.split()[0]):
            cmd,*args = cmd.split()
            getattr(src.cliect,cmd)(*args,soc)
            continue
        res = soc.recv(1024)
        print(res.decode('utf-8'))