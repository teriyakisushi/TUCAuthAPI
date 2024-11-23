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
        """
        获取登录后的URP教务系统的用户姓名, 返回用户姓名
        传入参数为文件路径时，is_file参数必须为True

        Args:
            source: 响应文本或响应文件路径
            is_file: 是否为文件路径，默认为False
        """
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
        """
        获取登录后的URP教务系统的用户绩点,返回用户的绩点
        传入参数为文件路径时，is_file参数必须为True

        Args:
            source: 响应文本或响应文件路径
            is_file: 是否为文件路径，默认为False
        """
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
        """
        获取本学期课程信息，返回原始json数据（未解析）

        Args:
            auth_instance(Auth): Auth实例
        """
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
        """
        获取课程时间，返回原始json数据（未解析）

        Args:
            auth_instance: Auth实例
        """
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
        """
        获取挂科的课程信息，返回原始json数据（未解析）

        Args:
            auth_instance(Auth): Auth实例
        """
        if not auth_instance.login_status:
            raise ValueError('请先登录！')

        try:
            res = auth_instance.requests.get(
                'http://stu.j.tjcu.edu.cn/student/integratedQuery/scoreQuery/unpassedScores/index',
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

    async def urp_get_scheme_score(self, auth_instance: TJCUAuth) -> str:
        """
        获取培养方案成绩，返回原始json数据（未解析）

        Args:
            auth_instance(Auth): Auth实例
        """
        if not auth_instance.login_status:
            raise ValueError('请先登录！')

        try:
            res = auth_instance.requests.get(
                'http://stu.j.tjcu.edu.cn/student/integratedQuery/scoreQuery/schemeScores/index',
            )
            Tools.save_response_text(res.text, 'scheme_response.txt', './Response')
            await asyncio.sleep(0.1)

            code = CodeParser.urp_find_schemescore_code('./Response/scheme_response.txt', is_file=True)

            url = f'http://stu.j.tjcu.edu.cn/student/integratedQuery/scoreQuery/{code}/schemeScores/callback'

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

    @staticmethod
    def urp_get_user_avatar(auth_instance: TJCUAuth, source: str = './Response/login_res.txt', is_file: bool = True) -> bytes:
        '''
        获取用户头像

        Args:
            source: 响应文本或响应文件路径
            is_file: 是否为文件路径，默认为False

        Returns:
            bytes: 用户头像的Bytes流
        '''
        if not source:
            raise ValueError('请求文本或文件路径不能为空！')

        if is_file:
            with open(source, 'rb') as f:
                source = f.read()
                source = source.decode('utf-8')

        # URL eg.  <img class="nav-user-photo" src="/main/queryStudent/img?xxxxxx>"
        avatar_url = re.search(r'<img class="nav-user-photo" src="(.*?)"', source)
        if avatar_url:
            avatar_url = avatar_url.group(1)
        else:
            raise ValueError('未找到用户头像URL！')

        try:
            res = auth_instance.requests.get(
                url=f'http://stu.j.tjcu.edu.cn{avatar_url}',
                headers={
                    'User-Agent': auth_instance.UA,
                }
            )
            return res.content
        except Exception as e:
            raise ValueError(f'Error: {e}')
