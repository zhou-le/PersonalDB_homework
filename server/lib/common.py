def login_in(user,login,conn):
    def wrapper(func):
        def login_plug(*args,**kwargs):
            if user['name']:
                func(*args,**kwargs)
            else:
                conn.send('先登录'.encode('utf-8'))