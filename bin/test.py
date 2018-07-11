import socket,json,os,struct
from conf import setting
soc = socket.socket()
soc.connect((setting.IP,setting.prot))

class cliect:
    @staticmethod
    def put(file_path, conn):
        file_name = os.path.basename(file_path)

        if not os.path.exists(file_path):
            print('找不到文件')
        else:
            headdic = cliect.make_head(file_path)

            head_size = cliect.get_head_size(headdic)
            conn.send(head_size)
            conn.send(headdic)
            # EVERY_TIME_SEND_SIZE = [20, 20, 30, ]
            with open(file_path, 'rb')as f:
                for line in f:
                    conn.send(line)

    @staticmethod
    def get(_,conn):
        head_size = struct.unpack('i', conn.recv(4))[0]
        print(head_size)
        head = json.loads(conn.recv(head_size))
        size = 0
        if not head['name']:
            print('无结果')
            return
        with open(head['name'], 'wb')as f:
            while size < head['total_size']:
                line = conn.recv(1024)
                f.write(line)
                size += len(line)

    @staticmethod
    def get_head_size( head_dic):
        return struct.pack('i', len(head_dic))

    @staticmethod
    def make_head(file_path):
        total_size = os.path.getsize(file_path)

        hashcode = cliect.get_hashcode(file_path,total_size)
        file_name = os.path.basename(file_path)

        head_dic = {
            'total_size': total_size,
            'name': file_name,
            'hashcode': hashcode
        }

        json_dic = json.dumps(head_dic)
        bytes_dic = json_dic.encode('utf-8')

        return bytes_dic

    @staticmethod
    def get_hashcode(file_path, total_size):
        import hashlib
        EVERY_TIME_SEND_SIZE = [20, 20, 30, 20]
        md5 = hashlib.md5()
        with open(file_path,'rb')as f:
            for i in EVERY_TIME_SEND_SIZE:
                md5.update(f.read(10))
                f.seek(total_size//i)
        return md5.hexdigest()


while True:
    cmd = input('<>>>>>>>>>>>')
    if len(cmd) == 0:
        continue
    soc.send(cmd.encode('utf-8'))
    if hasattr(cliect,cmd.split()[0]):
        cmd,*args = cmd.split()
        getattr(cliect,cmd)(*args,soc)
        continue
    res = soc.recv(1024)
    print(res.decode('utf-8'))