from conf import setting
import socketserver,sys,os
from core import user

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class server(socketserver.BaseRequestHandler):
    def handle(self):

        while True:
            cmd_world = self.request.recv(1024).decode('utf-8')
            cmd,*args = cmd_world.split()
            if hasattr(user.users, cmd):
                try:
                    getattr(user.users, cmd)(*args, self.request)
                except TypeError as e:
                    self.request.send('不正确的参数'.encode('utf-8'))
            else:
                self.request.send('无效的命令'.encode('utf-8'))




if __name__ == '__main__':

    soc = socketserver.ThreadingTCPServer((setting.IP,setting.prot),server)
    soc.serve_forever()