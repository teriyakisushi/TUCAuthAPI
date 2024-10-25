import os
import re
from datetime import datetime
from auth_request import TJCUAuth


def get_urp_info() -> str:

    request_dir = './Request'
    try:
        files = [os.path.join(request_dir, f) for f in os.listdir(request_dir) if f.endswith('.txt')]
        if not files:
            raise FileNotFoundError('没有请求文件喵')
        latest_file = max(files, key=os.path.getctime)

        with open(latest_file, 'r', encoding='UTF-8') as f:
            res_str = f.read()

        name = re.search(r'<span class="user-info">\s*<small>欢迎您，</small>\s*(.*?)\s*</span>', res_str)
        gpa = re.search(r'<span class="infobox-data-number" id="gpa">(.*?)</span>', res_str)

        info = f'请问是{name.group(1)}同学吗？\n你的绩点是{gpa.group(1)}哦！'

    except Exception as e:
        print(f'Error: {e}')
        return 'Error'
    return info


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

    usr = '20229988'
    pwd = '123456'

    URP = TJCUAuth(
        user=usr,
        pwd=pwd,
        target_url='http://stu.j.tjcu.edu.cn/'
    )
    res = URP.power_login()
    save_request_text(res)
    print(get_urp_info())
