[![PyPi Version](https://img.shields.io/pypi/v/akitools)](https://pypi.org/project/akitools/) [![License](https://img.shields.io/pypi/l/akitools)](https://pypi.org/project/akitools/)

 ##### Install

```
pip install akitools
```

##### Example

```python
>>> from akitools import ftime
>>> ftime()
'20191109'
>>> ftime(f=4)
'2019-11-09 13:12:04'
>>> ftime(t=1571940315)
'20191025'

>>> from akitools import ctime
>>> ctime('2017-01-01')
1483200000
```


* HEADER
* ftime
* ctime
* send_mail
* log_write