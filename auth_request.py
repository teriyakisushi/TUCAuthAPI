import re
import time
import execjs
import requests
from loguru import logger


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
            dict: 登录成功返回的页面信息
        '''

        salt, lt = self.get_salt()
        if not salt or not lt:
            return False

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
            return res.text

        except Exception as e:
            logger.error(f'Error: {e}')
            return False

    def power_login(self, user: str = '', pwd: str = '', target_url: str = '') -> str:
        '''
        获取渲染完成后的页面，可用在当前页面需要JavaScript渲染的情况

        Args:
            user: 学号
            pwd: 密码
            target_url: 需要访问的服务地址
        Returns:
            dict: 登录成功返回的页面信息
        '''
        from playwright.sync_api import sync_playwright

        if not user and not pwd:
            user = self.user
            pwd = self.pwd

        if not target_url:
            target_url = self.service_url

        url = self.auth_url + '?service=' + target_url

        info = f'Login User:{user}, Password:{pwd}, Target URL:{url}'
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
                    # page.wait_for_load_state('load')
                    page.goto(target_url)
                    page.wait_for_load_state('load')
                    # Waiting for the page to render
                    # page.wait_for_timeout(1500)
                    # page.wait_for_load_state('load')

                    # Check if login was successful
                    if "统一身份认证" in page.title():
                        logger.error("Login failed, still on login page.")
                        return "Login failed, still on login page."

                # Get the page content
                logger.info("Getting page content")
                content = page.content()
                browser.close()
                return content

        except Exception as e:
            logger.error(f'Error: {e}')
            return 'something error'
