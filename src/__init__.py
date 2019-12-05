"""Copyright (c) 2019 by aki
HEADER:         浏览器UA
ftime:          将时间戳转换成日期/时间字符串
ctime:          将日期/时间字符串转换成时间戳
filenameSub:    替换不符合文件名的字符
splitIterable:  将可迭代的数据分割成多个列表
mail:           发送邮件
logs:           日志写入
weather:        获取实时气象情况
ipInfo:         获取ip地址信息
"""

__version__ = '0.2.0'

from ._akitools import HEADER, ftime, ctime, filenameSub, splitIterable, mail, logs, weather, ipInfo