import sys
import os
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Auth.auth_request import TJCUAuth
from Utils.tools import Tools
from URP.urp_api import URP
from URP.parse import ExamList
from Config.settings import user, pwd


async def test_interface(Instance: TJCUAuth):
    MyURP = URP()
    unpass_exam_text = await MyURP.urp_get_unpass_course(auth_instance=Instance)
    print("Done") if Tools.save_response_text(
        unpass_exam_text,
        'unpass_exam.json',
        './Response'
    ) != -1 else print("Failed")

    MyUPExam = ExamList(
        source='./Response/unpass_exam.json',
        is_file=True
    )

    print("未通过的考试如下：")
    for ue in MyUPExam.current_unpassed_exams:
        print(f"课程名称：{ue.Name}")
        print(f"课程编号：{ue.Code}")
        print(f"考试时间：{ue.Date}")
        print(f"考试成绩：{ue.Score}")
        print(f"学期：{ue.Term}")
        print("-" * 30)

    print("曾经挂科的课程如下：")
    for ue in MyUPExam.past_unpassed_exams:
        print(f"课程名称：{ue.Name}")
        print(f"课程编号：{ue.Code}")
        print(f"考试时间：{ue.Date}")
        print(f"考试成绩：{ue.Score}")
        print(f"学期：{ue.Term}")
        print("-" * 30)


def main():

    SleepFox = TJCUAuth(
        user=user,
        pwd=pwd,
        target_url='http://stu.j.tjcu.edu.cn/'
    )

    SleepFox.power_login()  # save Session

    # 获取不及格考试信息
    asyncio.run(test_interface(Instance=SleepFox))


main()
