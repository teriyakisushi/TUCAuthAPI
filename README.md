

<h2 align="center">
天商统一身份认证登录服务API
</h2>

![dev environment](https://img.shields.io/badge/Dev%20Environment-Windows%2010-00adef?style=for-the-badge&logo=windows&logoColor=white)
![python version](https://img.shields.io/badge/Python-3.10-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![playwirght version](https://img.shields.io/badge/Playwright-1.48.0-57e8e7?style=for-the-badge&logo=playwright&logoColor=white)

## 目录

- [目录](#目录)
- [📖项目简介](#项目简介)
- [🚀安装依赖](#安装依赖)
- [📚使用方法](#使用方法)
- [🎦Demo](#demo)
- [📝Todo](#todo)
- [Update Log](#update-log)



## 📖项目简介

本 API 用于天商 **“统一身份认证”** 系统的快捷登录以获取目标服务的响应内容。


## 🚀安装依赖
首先确保你的Python版本为`3.8+` ，在项目目录下执行以下命令：

```shell
pip install -r requirements.txt
playwright install
```

## 📚使用方法

`./Auth/auth_request.py` 提供了两种登录方法：
- `login()`: 获取登录后返回的响应页面，适合静态资源
- `power_login()`: 获取渲染完成后的登录页面内容，如 **URP教务系统**


创建登录实例需要如下参数:
- `user`: 学号
- `pwd`: 密码
- `target_url`: 目标页面URL

**示例：**

```python
from Auth.auth_request import TJCUAuth

# 创建登录实例
URP = TJCUAuth(
    user='114514',
    pwd='1919810',
    target_url='http://stu.j.tjcu.edu.cn/'
)
res = URP.login()
print(res)
```


## 🎦Demo

本仓库提供了一个简单的Demo程序，演示了如何利用本API获取天商URP教务系统的姓名和绩点信息。

修改`settings.py`的`user`和`pwd`为你的学号和密码，然后使用如下命令运行：

```shell
python demo.py
```

如果一切正常，你会看到如下示例输出：

```shell
请问是SleepFox同学吗？
你的绩点是: 4.99 哦！
```

## 📝Todo

- [x] URP教务系统
- [x] 解析课程表，详细看 `Update Log`
- [ ] 获取成绩
- [ ] 潜在的Captcha认证
- [ ] Backend support
- [ ] More lang support: `Go && Node.js`

## Update Log

[**点我查看详细**](update_log.md)

如果这个项目对你有帮助， 欢迎点个Star⭐️，你的支持是我最大的动力喵~

