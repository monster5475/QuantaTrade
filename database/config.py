import os


class Config:
    """
    配置文件信息
    """
    @staticmethod
    def get_data_dir():
        """
        返回数据目录
        :return:
        """
        direction = 'data'
        return direction + os.sep
