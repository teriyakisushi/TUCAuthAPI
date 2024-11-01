import asyncio
from Auth.auth_request import TJCUAuth
from Utils.tools import Tools
from URP.urp_api import URP
from settings import user, pwd


async def get_my_course(Instance: TJCUAuth):
    if not Instance.login_status:
        # 登录教务系统
        Instance.power_login()

    # 实例化一个URP对象
    MyURP = URP()

    # 获取课程信息
    course_data = await MyURP.urp_get_courseSelect(Instance)

    # 将课程信息保存到本地
    Tools.save_response_text(
        course_data,
        'course_data.json',
        './Response'
    )


def get_my_info(Instance: TJCUAuth):

    res = Instance.power_login()

    # 将响应文本保存到本地
    file_name = 'login_res.txt'
    Tools.save_response_text(res, file_name, './Response')

    # 读取响应文本，获取用户姓名和绩点
    name = URP.urp_get_name('./Response/login_res.txt', is_file=True)
    gpa = URP.urp_get_gpa('./Response/login_res.txt', is_file=True)

    print(f'请问是{name}同学吗?\n你的绩点是{gpa}哦！')


def main():

    # 实例化一个Auth对象
    SleepFox = TJCUAuth(
        user=user,
        pwd=pwd,
        target_url='http://stu.j.tjcu.edu.cn/'
    )

    # 获取你的姓名和绩点
    print(get_my_info(SleepFox))

    # 获取你本学期的课程信息
    asyncio.run(get_my_course(SleepFox))


main()
