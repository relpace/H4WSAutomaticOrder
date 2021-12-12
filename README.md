# XSTAutomaticOrder
#### 如果你不是H4WS学生 需要自行更改SchoolNo
#### 本项目依赖于requests库
#### 初次使用请在终端运行`pip3 install requests`
## 功能
在校膳通平台上自动点餐。支持:
- 按套餐号点餐
- 随机点餐
- 匹配套餐名点餐(还在码)
## 使用方法
- 1.编辑config.ini如下，并置于main.py同目录下
- 2.运行main.py
### 最好配合定时任务使用
[mode]

order_mode=rand

#*rand为随机模式；code为按套餐号点餐模式*

[preferences]

code=A B A B A

dish=片儿川 肉丝炒面 狮子头

*#菜品名称和套餐号用空格分割*

[login]

username=你微信点餐平台绑定的账号 
#20届学生为2020+班级+两位数字(分班考名次？)不记得自己去https://xst.nfcpwl.com/wx/index.html 上试

#19届学生为学号（6位）

password=你的学号（6位）
