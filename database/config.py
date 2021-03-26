import os


class Config:
    """
    配置文件信息
    """
    @staticmethod
    def get_data_file_path(file_name):
        """
        返回数据文件路径
        :return:
        """
        direction = os.path.dirname(__file__) + os.sep + 'data'
        return direction + os.sep + file_name + '.db'
