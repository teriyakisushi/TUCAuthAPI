import sys
import os
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Auth.auth_request import TJCUAuth
from Utils.tools import Tools
from URP.urp_api import URP
from URP.parse import CourseList
from settings import user, pwd


async def test_interface(Instance: TJCUAuth):
    MyURP = URP()
    course_text = await MyURP.urp_get_courseSelect(auth_instance=Instance)
    print("Done") if Tools.save_response_text(
        course_text,
        'course.json',
        './Response'
    ) != -1 else print("Failed")

    MyCourse = CourseList(
        source='./Response/course.json',
        is_file=True
    )

    for course in MyCourse:
        print("找到课程如下：")
        print(f"课程名称：{course.Name}")
        print(f"课程代码：{course.Code}")
        print(f"课程性质：{course.Property}")
        print(f"任课教师：{course.Teacher}")
        print(f"上课周：{course.Week}")
        print(f"学分：{course.Unit}")

        if course.Detail:
            for detail in course.Detail:
                print(f"上课日：星期{detail.day}")
                print(f"教学楼：{detail.building}")
                print(f"教室：{detail.classroom}")
                for time in detail.timeDetail:
                    print(f"上课时间：{time['startTime']} - {time['endTime']}")
                print('*' * 30)
        else:
            print("该课程暂无上课时间和地点信息。")


def main():

    SleepFox = TJCUAuth(
        user=user,
        pwd=pwd,
        target_url='http://stu.j.tjcu.edu.cn/'
    )

    SleepFox.power_login()  # save Session

    # 获取课程信息
    asyncio.run(test_interface(Instance=SleepFox))


main()
