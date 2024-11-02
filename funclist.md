
## Auth.auth_request

- get_req

```python
def get_req(self,targert_url: str) -> None:
    '''
    获取请求，已弃用
    '''
```

- get_salt

```python
def get_salt(self) -> str:
    '''
    获取登录账户所需的salt值
    '''
```

- login

```python
def login(self, user: str = '', pwd: str = '') -> str:
    '''
    Args:
        user: 学号
        pwd: 密码
    Returns:
        str: 登录成功返回的页面信息
    '''
```

- power_login

```python
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
```

- clean_cookies

```python
def clean_cookies(self) -> None:
    '''
    清除cookies
    '''
```
