- **2024.11.1**: 
  - 将选课的每一门课程设为一个对象，包含属性见 ⬇ 底部折叠标签
  - 修改`settings.py` 中的 `course_timeDetail_method` 为 `0`会合并该课程的节次信息，直接显示该课程的开始-结束时间，为`1`则显示每一节的开始-结束时间
  - 使用示例（请先用`urp_get_courseSelect()`获取选课信息）

```python
from URP.CourseParse import CourseList

'''
创建你所选课程的对象，CourseList将读取响应文件的每一门课程并将其转换为一个课程对象，你可以方便的查看其属性值
'''
MyCourse = CourseList(
    source='/Response/course_data.json',
    is_file=True
)

for course in MyCourse:
    print("找到课程如下：")
    print(f"课程名称：{e.Name}")
    print(f"课程代码：{e.Code}")
    print(f"课程性质：{e.Property}")
    print(f"任课教师：{e.Teacher}")
    print(f"上课周：{e.Week}")
    print(f"学分：{e.Unit}")

    if e.Detail:
        for detail in e.Detail:
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
| timeDetial->sessionIndex | Int    | 节次          |
| timeDetial->startTime    | String | 开始时间      |
| timeDetial->endTime      | String | 结束时间      |

- **2024.10.28**
    - 新增两个方法`urp_get_courseSelect`和`urp_get_timeTable`，分别用于获取选课信息和时间表
    - 添加了`settings.py`文件，用于存放一些全局变量