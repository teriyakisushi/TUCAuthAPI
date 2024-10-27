import re
import time
import execjs
import requests
from loguru import logger

headers = {}
data = {}


class TJCUAuth:
    def __init__(self, user: str, pwd: str, target_url: str) -> None:
        '''
        Args:
            target_url: The service url that you want to access.
        '''
        self.user = user
        self.pwd = pwd
        self.requests = requests.Session()
        self.service_url = target_url
        self.auth_url = 'http://authserver.tjcu.edu.cn/authserver/login'
        self.Referer = self.auth_url + '?service=' + target_url
        self.login_status = False

        self.UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        self.encrypt = execjs.compile(open('encrypt.js', 'r', encoding='utf-8').read())

    def get_req(self, target_url: str) -> None:
        '''
        Arg:
            target_url: 需要访问的服务地址
        Return:
            None
        '''
        url = self.auth_url + '?service=' + target_url
        # by using session() method,  you can avoid adding cookies to the headers list.
        headers = {
            'Accept': self.Accept,
            'User-Agent': self.UA,
            'Connection': 'keep-alive',
            'Referer': self.Referer,
        }
        params = {'service': url}

        try:
            self.requests.get(
                self.auth_url,
                headers=headers,
                params=params
            )
        except Exception as e:
            logger.error(f'Error: {e}')

    def get_salt(self) -> str:
        url = self.auth_url
        headers = {
            'User-Agent': self.UA,
            'Referer': self.Referer,
        }
        params = {'service': self.service_url}
        try:
            res = self.requests.get(
                url,
                headers=headers,
                params=params
            )
            salt = re.findall(r'pwdDefaultEncryptSalt = "(.*?)";', res.text)[0]
            lt = re.findall('input type="hidden" name="lt" value="(.*?)"', res.text)[0]
            # print(salt, lt)
            logger.success("Get the salt and lt successfully!")
            return salt, lt

        except Exception as e:
            logger.error(f'Error: {e}')
            return 0, 0   # It can actually return None, the return value is just for debugging or logical judgment.

    def login(self, user: str = '', pwd: str = '') -> str:
        '''
        Args:
            user: 学号
            pwd: 密码
        Returns:
            str: 登录成功返回的页面信息
        '''
        global headers, data
        return_info = ''

        salt, lt = self.get_salt()
        if not salt or not lt:
            return_info = 'Salt or lt is None'

        if not user and not pwd:
            user = self.user
            pwd = self.pwd

        headers = {
            'User-Agent': self.UA,
            'Referer': self.Referer,
        }
        pwd = self.encrypt.call('encryptAES', pwd, salt)
        logger.success('Encrypt the password successfully!')
        data = {
            'username': user,
            'password': pwd,
            'lt': lt,
            'dllt': 'userNamePasswordLogin',
            'execution': 'e1s1',
            '_eventId': 'submit',
            'rmShown': '1',
        }
        try:
            res = self.requests.post(
                self.auth_url,
                headers=headers,
                data=data
            )
            # logger.warning(res.text)
            if '统一身份认证' in res.text:
                logger.error("登录失败，请检查用户名和密码是否正确")
                return_info = "登录失败，请检查用户名和密码是否正确"

            logger.success("Login successfully!")
            self.login_status = True
            return_info = res.text

        except Exception as e:
            logger.error(f'Error: {e}')
            return_info = 'something error'

        return return_info

    def power_login(self, user: str = '', pwd: str = '', target_url: str = '') -> str:
        '''
        获取渲染完成后的页面，可用在当前页面需要JavaScript渲染的情况

        Args:
            user: 学号
            pwd: 密码
            target_url: 需要访问的服务地址
        Returns:
            str: 登录成功返回的页面信息
        '''
        from playwright.sync_api import sync_playwright

        if not user and not pwd:
            user = self.user
            pwd = self.pwd

        if not target_url:
            target_url = self.service_url

        url = self.auth_url + '?service=' + target_url

        info = f'Now using Login-User:{user}, Password:{pwd}, Target URL:{url}'
        logger.info(info)

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                page.goto(url)
                page.wait_for_load_state('load')

                # Fill the login box
                if "统一身份认证" in page.title():
                    page.fill('input[id="username"]', user)
                    page.fill('input[id="password"]', pwd)
                    time.sleep(1)
                    page.click('button[type="submit"]')

                    page.goto(target_url)
                    page.wait_for_load_state('load')

                    # Check if login was successful
                    if "统一身份认证" in page.title():
                        logger.error("登录失败，请检查用户名和密码是否正确")
                        return "登录失败，请检查用户名和密码是否正确"

                    # Don't forget to set the login status = =
                    self.login_status = True

                # Get the page content
                logger.info("Getting page content")
                content = page.content()

                # Export cookies from browser
                cookies = context.cookies()
                browser.close()

                # Import cookies to self.requests
                for cookie in cookies:
                    self.requests.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

                return content

        except Exception as e:
            logger.error(f'Error: {e}')
            return 'something error'

    def schedule_provider(self):
        if not self.login_status:
            logger.error('Please login first!')
            return 'Please login first!'
        try:
            course_res = self.requests.get(
                url='http://stu.j.tjcu.edu.cn/student/courseSelect/thisSemesterCurriculum/ajaxStudentSchedule/curr/callback',
                cookies=self.requests.cookies
            )
            course_data = course_res.text
        except Exception as e:
            logger.error(f'Error: {e}')
            course_data = 'something error'

        return course_data

    def clean_cookies(self):
        self.requests.cookies.clear()
        logger.success('Clean the cookies successfully!')
