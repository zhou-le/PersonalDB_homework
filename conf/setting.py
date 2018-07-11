import os


home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
user_info = os.path.join(home,'PersonalDb','user_info')
DB = os.path.join(home,'PersonalDb','database')


IP = '127.0.0.1'
prot = 8080



disk = 10*1024*1024