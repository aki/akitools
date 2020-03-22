"""Copyright (c) 2019 by aki

tools.py
HEADER:                     浏览器UA
ftime:                      将时间戳转换成日期/时间字符串
ctime:                      将日期/时间字符串转换成时间戳
random_chinese_character:   随机中文字符，中文姓氏
random_password:            随机密码
filename_norm:              替换不符合文件名的字符
split_iterable:             将可迭代的数据分割成多个列表
mail:                       发送邮件
logs:                       日志写入
weather:                    获取实时气象情况
ip_info:                    获取ip地址信息

vk.py
VK:                         键盘虚拟码
"""

__version__ = '0.2.7'

from .tools import *
from .vk import VK
