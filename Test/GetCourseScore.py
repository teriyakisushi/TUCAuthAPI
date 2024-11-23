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

    score_text = await MyURP.urp_get_scheme_score(auth_instance=Instance)

    print("Done") if Tools.save_response_text(
        score_text,
        'scheme_score.json',
        './Response'
    ) != -1 else print("Failed")


def main():

    SleepFox = TJCUAuth(
        user=user,
        pwd=pwd,
        target_url='http://stu.j.tjcu.edu.cn/'
    )

    SleepFox.power_login()  # save Session

    # 获取成绩信息
    asyncio.run(test_interface(Instance=SleepFox))


main()
