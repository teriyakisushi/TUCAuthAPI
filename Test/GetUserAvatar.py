import sys
import os
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Auth.auth_request import TJCUAuth
from Utils.tools import Tools
from URP.urp_api import URP
from Config.settings import user, pwd


async def test_interface(Instance: TJCUAuth):

    MyURP = URP()
    img_res = MyURP.urp_get_user_avatar(Instance)
    Tools.bytes_to_img(byte_data=img_res, img_path='./Response/avatar.jpg')
    print('Done') if os.path.exists('./Response/avatar.jpg') else print('Failed')


def main():

    SleepFox = TJCUAuth(
        user=user,
        pwd=pwd,
        target_url='http://stu.j.tjcu.edu.cn/'
    )

    res = SleepFox.power_login()
    Tools.save_response_text(
        res,
        'login_res.txt',
        './Response'
    )
    # 获取用户头像
    asyncio.run(test_interface(Instance=SleepFox))


main()
