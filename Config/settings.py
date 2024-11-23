'''
Planning to use this file to set some global variables
'''

# Target URL
urp_url = 'http://stu.j.tjcu.edu.cn/'
peexam_url = 'http://peexam.tjcu.edu.cn/'


# User Info
user = ''
pwd = ''

# File Path
response_path = './Response'

# File Name
login_res = 'login_res.txt'
courseSelect_res = 'courseInfo.json'
peexam_res = 'peexam.json'

# Course Parse

'''
课程表数据解析方法:
0: 合并节次, 显示开始到结束的时间
1: 分开节次，显示每个节次的开始时间和结束时间
'''
course_timeDetail_combine = 0
