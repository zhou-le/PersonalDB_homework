from PersonalDb import db_handle
from conf import setting
import os, json, struct, subprocess


class data:
    @classmethod
    def read_from_userinfo_db(cls, name):
        '''
        从文件中将对象读取出来
        :param name: 用户名
        :return: 用户对象
        '''
        return db_handle.reader(name)

    def save(self):
        '''
        保存对象
        :return:无
        '''
        db_handle.write(self)


class user(data):
    '''
    负责用户的创建改变密码
    '''
    def __init__(self, name, passwd):
        '''
        注册实例化之后自动存储
        :param name:用户名
        :param passwd: 密码
        disk_size:为用户磁盘配额
        '''
        self.name = name
        self.passwd = passwd
        self.disk_size = setting.disk
        self.save()

    def change_passwd(self, passwd):
        '''
        修改密码
        :param passwd:用户要修改的密码
        :return: 无
        '''
        self.passwd = passwd
        self.save()


class PersonDbModel:

    def __init__(self, name):
        '''
        初始化个人本地库，根据用户名来建立用户的db库和一些常用路径
        :param name:用户名
        '''
        self.current_db_path = os.path.join(setting.DB, name)
        self.db_path = os.path.join(setting.DB, name)
        self.hashcode_conf = os.path.join(self.db_path, 'hashcode_conf')
        if os.path.exists(self.hashcode_conf):
            with open(self.hashcode_conf,'w')as f:
                json.dump({},f)
        if not os.path.exists(self.db_path):
            os.mkdir(self.db_path)



    def mkdir(self, dir_name, conn):
        '''
        建立文件夹
        :param dir_name:文件夹的名字
        :param conn: 套接字对象，用于发送结果
        :return:
        '''
        dir_path = os.path.join(self.current_db_path, dir_name)
        if os.path.isdir(dir_path):
            conn.send('建立失败文件夹已存在'.encode('utf-8'))
        else:
            os.mkdir(dir_path)
            conn.send('建立成功'.encode('utf-8'))

    def rmdir(self, dir_name, conn):
        '''

        :param dir_name:要删除的文件夹
        :param conn: 套接字对象
        :return:
        '''
        dir_path = os.path.join(self.current_db_path, dir_name)
        if os.path.isdir(dir_path):
            try:
                os.rmdir(dir_path)
                conn.send('删除成功'.encode('utf-8'))
            except Exception:
                conn.send('空文件夹不可直接删除'.encode('utf-8'))
        else:
            conn.send('删除失败文件夹不存在'.encode('utf-8'))

    def rmfile(self, file_name, conn):
        '''

        :param file_name: 要删除的文件名
        :param conn: 套接字对象
        :return:
        '''
        file_path = os.path.join(self.current_db_path, file_name)

        if os.path.exists(file_path) and os.path.isdir(file_path):
            os.rmdir(file_path)
            conn.send('删除成功'.encode('utf-8'))


        else:
            conn.send('删除失败文件夹不存在'.encode('utf-8'))




    def ls(self, conn):
        '''
        列出当前文件夹下的所有的文件或文件夹
        :param conn: 套接字对象
        :return:
        '''
        dirlist = os.listdir(self.current_db_path)
        res = ''
        for i in range(len(dirlist)):
            res += '%-6s' % dirlist[i]
            if (i + 1) % 5 == 0:
                res += '\n'
        conn.send(res.encode('utf-8'))




    def get(self, file_name, conn):
        '''
        用户获取文件
        :param file_name: 当前文件下的文件名，
        :param conn: 套接字对象
        :return:
        '''
        file_abs_path = os.path.join(self.current_db_path, file_name)
        print(file_abs_path)
        if not os.path.exists(file_abs_path):
            headdic = json.dumps({'name': None})
            head_size = self.get_head_size(headdic)
            conn.send(head_size)
            conn.send(headdic.encode('utf-8'))

        else:
            headdic = self.make_head(file_name)
            head_size = self.get_head_size(headdic)
            conn.send(head_size)
            conn.send(headdic)
            with open(file_abs_path, 'rb')as f:
                for line in f:
                    conn.send(line)

    def get_head_size(self, head_dic):
        '''
        获取文件头的大小
        :param head_dic:文件头
        :return: len（文件头）
        '''
        return struct.pack('i', len(head_dic))




    def make_head(self, name):
        '''
        制作报头,
        :param name:文件名
        :return: 文件报头，{'total_size':...,'name':....,'hashcode':....,}
        '''
        total_size = os.path.getsize(os.path.join(self.current_db_path, name))

        hashcode = self.get_hashcode(name)
        file_name = name

        head_dic = {
            'total_size': total_size,
            'name': file_name,
            'hashcode': hashcode
        }

        json_dic = json.dumps(head_dic)
        bytes_dic = json_dic.encode('utf-8')

        return bytes_dic

    def get_hashcode(self, name):
        '''
        获取文件的hashcode
        :param name: 当前路径的文件
        :return: hashcode
        '''

        import hashlib
        EVERY_TIME_SEND_SIZE = [20, 20, 30, 20]
        md5 = hashlib.md5()
        total_size = os.path.getsize(os.path.join(self.current_db_path,name))
        with open(os.path.join(self.current_db_path,name),'rb' )as f:

            for i in EVERY_TIME_SEND_SIZE:
                md5.update(f.read(10))
                f.seek(total_size // i)
        return md5.hexdigest()



    def put(self, conn):
        '''
        上传文件
        :param conn:套接字对象
        :return: 无
        '''
        head_size = struct.unpack('i', conn.recv(4))[0]
        print(head_size)
        head = json.loads(conn.recv(head_size).decode('utf-8'))
        size = 0
        file_path = os.path.join(self.current_db_path,head['name'])
        with open(file_path, 'wb')as f:
            while size < head['total_size']:
                line = conn.recv(1024)
                f.write(line)
                size += line


