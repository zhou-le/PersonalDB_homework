from PersonalDb import DB_MODULE


class users:
    user = {'name': None}
    userdisk = {'disk': None}
    @staticmethod
    def register(name,passwd, conn):
        user = DB_MODULE.user.read_from_userinfo_db(name)
        if user:
            conn.secd('用户已经存在'.encode('utf-8'))
        else:
            DB_MODULE.user(name,passwd)

            conn.send('注册成功'.encode('utf-8'))
    @staticmethod
    def login(name, passwd, conn):
        user = DB_MODULE.user.read_from_userinfo_db(name)
        if user:
            if user.passwd == passwd:
                conn.send('登陆成功'.encode('utf-8'))
                users.user['name'] = name
                users.userdisk['disk'] = DB_MODULE.PersonDbModel(name)
            else:
                conn.send('密码错误'.encode('utf-8'))
        else:
            conn.send('找不到用户'.encode('utf-8'))

    @staticmethod
    def put(_,conn):
        users.userdisk['disk'].put(conn)

    @staticmethod
    def get(file_path, conn):
        users.userdisk['disk'].get(file_path, conn)

    @staticmethod
    def ls(conn):
        users.userdisk['disk'].ls(conn)

    @staticmethod
    def mkdir(dir_name, conn):
        users.userdisk['disk'].mkdir(dir_name, conn)

    @staticmethod
    def rmdir(dir_name, conn):
        users.userdisk['disk'].rmdir(dir_name, conn)

    @staticmethod
    def rmfile(file_name, conn):
        users.userdisk['disk'].rmfile(file_name, conn)
