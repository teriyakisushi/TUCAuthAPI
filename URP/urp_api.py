import re
import asyncio
from Auth.auth_request import TJCUAuth
from .parse import CodeParser
from Utils.tools import Tools


class URP:
    def __init__(self):
        pass

    @staticmethod
    def urp_get_name(source: str, is_file: bool = False) -> str:
        '''
        获取登录后的URP教务系统的用户姓名
        传入参数为文件路径时，is_file参数必须为True

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
        传入参数为文件路径时，is_file参数必须为True

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

    async def urp_get_courseSelect(self, auth_instance: TJCUAuth) -> str:
        '''
        获取本学期课程信息，返回json数据
        '''
        if not auth_instance.login_status:
            raise ValueError('请先登录！')

        res = auth_instance.requests.get(
            'http://stu.j.tjcu.edu.cn/student/courseSelect/thisSemesterCurriculum/index',
        )
        Tools.save_response_text(res.text, 'schedule_response.txt', './Response')
        await asyncio.sleep(0.1)

        plan_code = CodeParser.urp_find_semester_plancode('./Response/schedule_response.txt', is_file=True)

        url = f'http://stu.j.tjcu.edu.cn/student/courseSelect/thisSemesterCurriculum/{plan_code}/ajaxStudentSchedule/curr/callback'

        res = auth_instance.requests.get(
            url=url,
            headers={
                'User-Agent': auth_instance.UA,
                'Referer': 'http://stu.j.tjcu.edu.cn/student/courseSelect/thisSemesterCurriculum/index'
            }
        )
        return res.text

    async def urp_get_courseTime(self, auth_instance: TJCUAuth) -> str:
        '''
        获取课程时间，返回json数据

        Args:
            auth_instance: Auth实例

        Returns:
            str: 课程时间的json数据
        '''
        if not auth_instance.login_status:
            raise ValueError('请先登录！')

        try:
            res = auth_instance.requests.get(
                url='http://stu.j.tjcu.edu.cn/ajax/getSectionAndTime?ff=f'
            )
            return res.text

        except Exception as e:
            raise ValueError(f'Error: {e}')

    async def urp_get_unpass_course(self, auth_instance: TJCUAuth) -> str:
        '''
        获取挂科的课程信息，返回json数据

        Args:
            auth_instance: Auth实例

        Returns:
            str: 未通过的课程信息的json数据
        '''
        if not auth_instance.login_status:
            raise ValueError('请先登录！')

        try:
            res = auth_instance.requests.get(
                'http://stu.j.tjcu.edu.cn/student/integratedQuery/scoreQuery/index',
            )
            Tools.save_response_text(res.text, 'unpass_response.txt', './Response')
            await asyncio.sleep(0.1)

            code = CodeParser.urp_find_unpassexam_code('./Response/unpass_response.txt', is_file=True)

            url = f'http://stu.j.tjcu.edu.cn/student/integratedQuery/scoreQuery/{code}/unpassed/scores/callback'

            res = auth_instance.requests.get(
                url=url,
                headers={
                    'User-Agent': auth_instance.UA,
                    'Referer': 'http://stu.j.tjcu.edu.cn/student/integratedQuery/scoreQuery/index'
                }
            )
            return res.text

        except Exception as e:
            raise ValueError(f'Error: {e}')
