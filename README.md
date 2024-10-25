<h2 align="center">
天商校园验证服务API
</h2>

### Description

本API提供天商“统一身份认证”服务的接口，用于快捷登录操作。

### Installation
首先确保你的Python版本位于`3.8+`，然后执行以下命令安装依赖：

```shell
pip install -r requirements.txt
playwright install
```

`playwright`用于等待目标页面渲染完成，以便获取页面内容，若你需要访问的 `target_url` 为静态页面，可以不安装。

### Usage

`auth_request.py` 提供了两种快捷登录方法
- `login()`: 获取登录后返回的页面响应，适合静态页面
- `power_login()`: 使用`playwright`获取登录后的页面内容，适合动态页面，比如 **URP教务系统**

创建该实例需要如下参数:
- `user`: 学号
- `password`: 密码
- `target_url`: 目标页面的URL

**使用方法：**

```python
# 创建AuthRequest对象
URP = TJCUAuth(
    usr='你的学号',
    pwd='你的密码',
    target_url='目标页面的URL'
)
res = URP.login()
print(res)
```

### Demo

本仓库提供了一个简单的Demo，用于演示如何使用该API，
修改`demo.py`的`usr`和`pwd`为你的学号和密码，然后使用如下命令运行：

```shell
python demo.py
```

如果一切正常，你会看到如下示例输出：

```shell
请问是SleepFox同学吗？
你的绩点是: 4.99 哦！
```

### TO DO

- [ ] 添加潜在的Captha验证
- [ ] 更多的登录场景
- [ ] 更多&更快捷的信息查询方法