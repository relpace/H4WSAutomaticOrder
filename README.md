# XSTAutomaticOrder
#### 如果你不是H4WS学生 需要自行更改SchoolNo
## 功能
在校膳通平台上自动点餐。支持:
- 按套餐号点餐
- 随机点餐
- 匹配套餐名点餐(还在码)





### 配置方法
编辑config.ini，并置于main.py同目录下

[mode]

order_mode=rand

#*rand为随机模式；code为按套餐号点餐模式*

[preferences]

code=A B A B A

dish=片儿川 肉丝炒面 狮子头

*#菜品名称和套餐号用空格分割*
