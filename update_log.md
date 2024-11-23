- **2024.11.23**:
  - 调整了一下项目结构，将`settings.py`移动到`Config`目录下
  - `URP.parse`新增`SchemeExam`及其子类，用于解析培养方案的考试信息
  - 原`Exam`类更名为`UPExam`，适用于其所有子类
  - 计划：`settings.py` -> `config.json`，将配置文件改为json格式，方便读取和修改

- **2024.11.22**:
  - `URP.urp_api`新增方法: `urp_get_scheme_score()`, 用于获取培养方案成绩
  - `URP.parse.CodeParser` 新增方法: `urp_find_scheme_code()`, 用于获取培养方案url的code

- **2024.11.20**:
  - 新增方法: `urp_get_user_avatar()`, 用于获取用户头像(一般是你的照片)
  - 为`Utils.Tools`类新增静态方法`bytes_to_image()`，用于将字节流转换为图片文件

**获取用户头像示例：**

```python
MyURP = URP()

# 获取用户头像，需要提供URP实例
img_res = MyURP.urp_get_user_avatar(auth_instance)

# 将字节流写入为图像文件
Tools.bytes_to_img(
  byte_data=img_res, 
  img_path='./Response/avatar.jpg'
  )

print('Done') if os.path.exists('./Response/avatar.jpg')
```


- **2024.11.18**:
  - 将未通过课程的信息存储在`Exam`对象中，包含属性见 ⬇ 底部折叠标签
  - `Exam`类成员含 `current_unpassed_exams` 和 `past_unpassed_exams`，分别存储当前未通过的课程和曾经未通过的课程
  - 使用示例（请先用`urp_get_unpass_course()`获取未通过课程信息）

```python
from URP.parse import ExamList

'''
先确保你已经获取了未通过的考试信息(urp_get_unpass_course)，然后可打印其属性值
'''

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
```

- 你可以使用`toString()`方法将对象转换为json格式的字符串，如`MyUPExam.toString()`，返回内容如下：

```json
{
    "current_unpassed_exams": [
        {
            "Name": "沟槽的申金网课",
            "Name_EN": "Online Course you ",
            "Code": "114514",
            "Score": 48.0,
            "Term": "2022-2023-2",
            "Date": "20230620"
        }
    ],
    "past_unpassed_exams": [
        {
            "Name": "大学物理A",
            "Name_EN": "College Physics A",
            "Code": "1919810",
            "Score": 59.0,
            "Term": "2022-2023-2",
            "Date": "20230621"
        }
    ]
}
```

---
Object Properties:

| 考试属性 | 类型   | 说明     |
| -------- | ------ | -------- |
| Name     | String | 课程名称 |
| Name_EN  | String | 英文名称 |
| Code     | String | 课程代码 |
| Score    | Float  | 考试成绩 |
| Term     | String | 学期     |
| Date     | String | 考试时间 |



- **2024.11.4**:
  - New class: `Exam`, used to get exam information, including passed and unpassed exams
  - Remove `CourseList.to_dict()` and `Course.to_dict()`, this method now herited from `BaseModel` method

- **2024.11.2**:
  - 新增方法: `urp_get_unpassed_course()`, 用于获取未通过的课程信息，`parse`方法尚未实现 

- **2024.11.1**: 
  - 将选课的每一门课程设为一个对象，包含属性见 ⬇ 底部折叠标签
  - 修改`settings.py` 中的 `course_timeDetail_method` 为 `0`会合并该课程的节次信息，直接显示该课程的开始-结束时间，为`1`则显示每一节的开始-结束时间
  - 使用示例（请先用`urp_get_courseSelect()`获取选课信息）

```python
from URP.parse import CourseList

'''
创建你所选课程的对象，CourseList将读取响应文件的每一门课程并将其转换为一个课程对象，你可以方便的查看其属性值
'''
MyCourse = CourseList(
    source='/Response/course_data.json',
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

```

- 你可以使用`toString()`方法将课程对象转换为json格式的字符串，如`MyCourse.toString()`，返回内容如下：

```json
[
  {
    "Name": "算法设计", // 课程名称
    "Code": "007",   // 课程代码
    "Property": "必修",  // 课程性质
    "Teacher": "睡狐",  // 任课教师
    "Unit": "3",  // 学分
    "Week": "1-16周", // 上课周数
    "Detail": [   // 上课时间与所在的教学楼、教室
      {
        "day": "1", // 星期几
        "building": "3号教学楼",  // 教学楼/实验室
        "classroom": "301",  // 教室
        "sessionStart": "1",  // 开始节次
        "sessionContinue": "2", // 持续节次
        "timeDetial": [
          {
            "sessionIndex": "1",  // 节次
            "startTime": "08:00",
            "endTime": "08:45"
          },
          {
            "sessionIndex": "2",  
            "startTime": "08:55",
            "endTime": "09:40"
          }
        ]
      },
      {
        "day": "3",
        "building": "7号教学楼",
        "classroom": "302",
        "sessionStart": "5",
        "sessionContinue": "2",
        "timeDetial": [
          {
            "sessionIndex": "5",
            "startTime": "13:30",
            "endTime": "14:15"
          },
          {
            "sessionIndex": "6",
            "startTime": "14:20",
            "endTime": "15:05"
          }
        ]
      }
    ]
  }
]
```

---

Object Properties:

| 课程属性                 | 类型   | 说明          |
| ------------------------ | ------ | ------------- |
| Name                     | String | 课程名称      |
| Code                     | String | 课程代码      |
| Property                 | String | 课程性质      |
| Teacher                  | String | 任课教师      |
| Unit                     | Float  | 学分          |
| Week                     | String | 上课周数      |
| Detail->day              | Int    | 星期几        |
| Detail->building         | String | 教学楼/实验室 |
| Detail->classroom        | String | 教室          |
| Detail->sessionStart     | Int    | 开始节次      |
| Detail->sessionContinue  | Int    | 持续节次      |
| timeDetail->sessionIndex | Int    | 节次          |
| timeDetail->startTime    | String | 开始时间      |
| timeDetail->endTime      | String | 结束时间      |

- **2024.10.28**
    - 新增两个方法`urp_get_courseSelect`和`urp_get_timeTable`，分别用于获取选课信息和时间表
    - 添加了`settings.py`文件，用于存放一些全局变量
