import os
import re


class Tools:
    def __init__(self):
        pass

    @staticmethod
    def save_response_text(res_txt: str = '', file_name: str = '', save_path: str = '') -> None:
        '''
        保存请求文本到本地

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
    def urp_get_name(source: str, is_file: bool = False) -> str:
        '''
        获取登录后的URP教务系统的用户姓名
        不能同时传入两个参数，请选择其中一个传入

        Args:
            source: 响应文本或响应文件路径

        Returns:
            str: 用户姓名
        '''
        user_name = ''

        if not source:
            raise ValueError('请求文本或文件路径不能为空！')

        if is_file:
            with open(source, 'r', encoding='UTF-8') as f:
                source = f.read()

        name = re.search(r'<span class="user-info">\s*<small>欢迎您，</small>\s*(.*?)\s*</span>', source)
        if name:
            user_name = name.group(1)
        else:
            raise ValueError('未找到用户姓名！')

        return user_name

    @staticmethod
    def urp_get_gpa(source: str, is_file: bool = False) -> float:
        '''
        获取登录后的URP教务系统的用户绩点
        不能同时传入两个参数，请选择其中一个传入

        Args:
            source: 响应文本或响应文件路径

        Returns:
            float: 用户绩点
        '''
        user_gpa = 0.0

        if not source:
            raise ValueError('请求文本或文件路径不能为空！')

        if is_file:
            with open(source, 'r', encoding='UTF-8') as f:
                source = f.read()

        gpa = re.search(r'<span class="infobox-data-number" id="gpa">(.*?)</span>', source)
        if gpa:
            user_gpa = float(gpa.group(1))
        else:
            raise ValueError('未能找到用户绩点')

        return user_gpa
