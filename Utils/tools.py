import os
# import json


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
    def urp_courseInfo_parse(source: str, is_file: bool = False) -> dict:
        '''
        解析课程表的json数据

        Args:
            source: 响应文本或响应文件路径

        Returns:
            dict: 课程表的json数据
        '''
        if not source:
            raise ValueError('请求文本或文件路径不能为空！')

        if is_file:
            with open(source, 'r', encoding='UTF-8') as f:
                source = f.read()

        ...

    @staticmethod
    def bytes_to_img(byte_data: bytes, img_path: str) -> None:
        '''
        将字节流数据保存为图片

        Args:
            byte_data: 图片的字节流数据
            img_path: 图片保存的路径
        '''
        with open(img_path, 'wb') as f:
            f.write(byte_data)
            print(f'Save the image to {img_path} successfully!')