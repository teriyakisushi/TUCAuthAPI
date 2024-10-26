import os
import re


class Tools:
    def __init__(self):
        pass

    @staticmethod
    def save_response_text(res_txt: str = '', file_name: str = '', save_path: str = '') -> None:
        '''
        将

        Args:
            res_txt: 响应文本
            file_name: 所需保存的文件名，默认保存到当前目录下的Response文件夹中
            save_path: 保存的路径，默认为当前目录下的Response文件夹中

        '''
        if not res_txt or not file_name:
            raise ValueError('请求文本或文件名不能为空！')

        if not save_path:
            save_path = './Response'

        os.makedirs(save_path, exist_ok=True)
        file_path = os.path.join(save_path, file_name)
        with open(file_path, 'w', encoding='UTF-8') as f:
            f.write(res_txt)
            print(f'Save the request text to {file_path} successfully!')

    @staticmethod
    def urp_get_name(res_str: str = '', res_file_path: str = '') -> str:
        '''
        获取登录后的URP教务系统的用户姓名
        不能同时传入两个参数，请选择其中一个传入

        Args:
            res_str: str: 响应文本
            res_file_path: str: 响应文本的文件路径

        Returns:
            str: 用户姓名
        '''
        user_name = ''

        if not res_str or not res_file_path:
            raise ValueError('请求文本或文件路径不能为空！')

        if res_str and res_file_path:
            raise ValueError('不能同时传入两个参数，请选择其中一个传入!')

        if res_str:
            name = re.search(r'<span class="user-info">\s*<small>欢迎您，</small>\s*(.*?)\s*</span>', res_str)
            user_name = name.group(1)

        if res_file_path:
            with open(res_file_path, 'r', encoding='UTF-8') as f:
                res_str = f.read()
            name = re.search(r'<span class="user-info">\s*<small>欢迎您，</small>\s*(.*?)\s*</span>', res_str)
            user_name = name.group(1)

        return user_name
