[![PyPi Version](https://img.shields.io/pypi/v/akitools)](https://pypi.org/project/akitools/) [![License](https://img.shields.io/pypi/l/akitools)](https://pypi.org/project/akitools/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/akitools)

 ##### Install

```
pip install akitools
```

##### Example

```python
>>> from akitools import ftime
>>> ftime()
'20191109'

>>> from akitools import ctime
>>> ctime('2017-01-01')
1483200000
```

|名称               |类型   |返回值 |简介
|-                  |-      |-      |---------
|HEADER             |常量   |dict   |浏览器UA
|ftime              |函数   |str    |时间戳转换成日期/时间字符串
|ctime              |函数   |int    |日期/时间字符串转换成时间戳
|mail               |函数   |None   |发送邮件
|logs               |函数   |None   |日志写入
|weather            |函数   |dict   |天气气象信息
|ip                 |函数   |dict   |IP地址信息
