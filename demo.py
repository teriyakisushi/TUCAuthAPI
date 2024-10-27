import os
from datetime import datetime
from auth_request import TJCUAuth
from tools import Tools


def save_request_text(res_str: str) -> None:
    current_time = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

    # Make sure directory exists ^_^
    os.makedirs('./Request', exist_ok=True)

    # Save the request text to local
    file_path = f'./Request/{current_time}.txt'
    with open(file_path, 'w', encoding='UTF-8') as f:
        f.write(res_str)
        print(f'Save the request text to {file_path} successfully!')


if __name__ == '__main__':

    user = '114514'
    pwd = '1919810'

    URP = TJCUAuth(
        user=user,
        pwd=pwd,
        target_url='http://stu.j.tjcu.edu.cn/'
    )
    res = URP.power_login()

    # 将响应文本保存到本地
    file_name = 'login_res.txt'
    Tools.save_response_text(res, file_name, './Response')

    # 读取响应文本，获取用户姓名和绩点
    name = Tools.urp_get_name('./Response/login_res.txt', is_file=True)
    gpa = Tools.urp_get_gpa('./Response/login_res.txt', is_file=True)

    print(f'请问是{name}同学吗?\n你的绩点是{gpa}哦！')
