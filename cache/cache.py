import pickle
import os


class Cache:
    """
    自定义的cache实现 持久化方式
    """
    cache_dict = dict()
    data_file_name = 'data.pkl'
    data_path = os.path.dirname(__file__) + os.sep + data_file_name

    @classmethod
    def set_data_file(cls, file_name):
        """
        设置cache文件名，并新建
        :param file_name:
        :return:
        """
        cls.data_file_name = file_name
        cls.data_path = os.path.dirname(__file__) + os.sep + cls.data_file_name
        if not os.path.exists(cls.data_path):
            file = open(cls.data_path,'w')
            file.close()

    @classmethod
    def get_dict(cls):
        """
        获取cache中的对象
        :return: 词典的方式返回
        """
        if os.path.getsize(cls.data_path):
            with open(cls.data_path, 'rb') as out_data:
                cls.cache_dict = pickle.load(out_data)
        return cls.cache_dict

    @classmethod
    def save_dict(cls, dic):
        """
        保存dic 对象到持久化文件中
        :param cls:
        :param dic:
        :return:
        """
        if dic is not None:
            cls.cache_dict = dic
        with open(cls.data_path, 'wb') as in_data:
            pickle.dump(cls.cache_dict, in_data)
        return True
