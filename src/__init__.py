"""Copyright (c) 2019 by aki

tools.py
HEADER:             浏览器UA
ftime:              将时间戳转换成日期/时间字符串
ctime:              将日期/时间字符串转换成时间戳
filename_norm:      替换不符合文件名的字符
split_iterable:     将可迭代的数据分割成多个列表
mail:               发送邮件
logs:               日志写入
weather:            获取实时气象情况
ip_info:            获取ip地址信息

vk.py
VK:                 键盘虚拟码
"""

__version__ = '0.2.4'

from .tools import HEADER, ftime, ctime, filename_norm, split_iterable, mail, logs, weather, ip_info
from .vk import VK
