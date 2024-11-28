from Auth.auth_request import TJCUAuth
from Utils.tools import Tools
from URP.urp_api import URP
from Config.settings import user, pwd


def get_my_info(Instance: TJCUAuth):

    res = Instance.power_login()

    # 将响应文本保存到本地
    res_file = 'login_res.txt'
    Tools.save_response_text(res, res_file, './Response')

    # 读取响应文本，获取用户姓名和绩点
    name = URP.urp_get_name(f'./Response/{res_file}', is_file=True)
    gpa = URP.urp_get_gpa(f'./Response/{res_file}', is_file=True)

    print(f'请问是{name}同学吗?\n你的绩点是{gpa}哦！')


def main():

    # 实例化一个Auth对象
    SleepFox = TJCUAuth(
        user=user,
        pwd=pwd,
        target_url='http://stu.j.tjcu.edu.cn/'
    )

    # 获取你的姓名和绩点
    print(get_my_info(Instance=SleepFox))


main()
