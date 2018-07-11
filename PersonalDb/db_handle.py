import pickle,os
from conf import setting

def reader(name):
    '''
    读取文件中的对象
    :param name:
    :return: 返回文件中的对象
    '''
    user_file = os.path.join(setting.user_info,'%s.pkl'%name)
    if not os.path.exists(user_file):
        return None
    with open(user_file,'rb')as f:
        return pickle.load(f)




def write(self):
    '''

    :param self:
    :return:
    '''
    user_path = os.path.join(setting.user_info,'%s.pkl'%self.name)
    with open(user_path,'wb')as f:
        pickle.dump(self,f)