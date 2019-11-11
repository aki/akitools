# Copyright (c) 2019 aki
"""
HEADER      常量  浏览器头部信息
ftime       函数  将时间戳转换成日期/时间字符串
ctime       函数  将日期/时间字符串转换成时间戳
send_mail   函数  发送邮件
log_write   函数  日志写入
"""
__all__ = ['HEADER', 'ftime', 'ctime', 'send_mail', 'log_write']


__version__ = '0.0.19'


HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}


def ftime(f: int = None, t: int = None, c: str = None) -> str:
    """
    将时间戳转换成日期/时间字符串

        f: 已知的格式               # 为空则默认为 1 ,返回格式为: 20140320
        t: 时间戳数字               # 为空则默认为 当前时间的时间戳
        c: 自定义格式               # 参考 '%Y%m%d' 格式
        如果参数f 与 c 都非空，则优先选择参数c 自定义的时间格式
            f = 1   return  20140320
            f = 2   return  2014.03.20
            f = 3   return  2014-03-20
            f = 4   return  2014/03/20
            f = 5   return  20140320 102824
            f = 6   return  2014.03.20 10:28:24
            f = 7   return  2014-03-20 10:28:24
            f = 8   return  2014/03/20 10:28:24
    """
    import time

    KNOWN_FORMATS = {
        1: '%Y%m%d',                    # 20140320
        2: '%Y.%m.%d',                  # 2014.03.20
        3: '%Y-%m-%d',                  # 2014-03-20
        4: '%Y/%m/%d',                  # 2014/03/20
        5: '%Y%m%d %H%M%S',             # 20140320 102824
        6: '%Y.%m.%d %H:%M:%S',         # 2014.03.20 10:28:24
        7: '%Y-%m-%d %H:%M:%S',         # 2014-03-20 10:28:24
        8: '%Y/%m/%d %H:%M:%S',         # 2014/03/20 10:28:24
    }

    t = t if t else time.time()
    if c:
        return time.strftime(c, time.localtime(t))
    return time.strftime(KNOWN_FORMATS.get(f, KNOWN_FORMATS[1]), time.localtime(t))


def ctime(d: str = None) -> int:
    """
    将日期/时间字符串转换成时间戳

        d:  日期/时间字符串               # 20140320
    """

    import time
    from dateutil.parser import parse

    if d:
        return int(parse(d).timestamp())
    return int(time.time())


def send_mail(recipient: list, subject: str, text: str):
    """
    发送邮件
        recipient       # 邮件收件人列表
        subject         # 邮件主题
        text            # 邮件内容
    """
    from email.mime.text import MIMEText
    from email.header import Header
    import smtplib

    message = MIMEText(text, 'plain', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail("", recipient, message.as_string())
    except Exception as e:
        print(e)


def log_write(filename: str, logs: str, filemode: str = 'a', level: int = 30, disable: bool = False):
    """
    日志写入
        filename        # 日志文件名
        logs            # 日志内容
        filemode        # 写入模式      a w
        level           # 日志模式      CRITICAL=50 FATAL=50 ERROR=40 WARNING=30 WARN=30 INFO=20 DEBUG= 0 NOTSET=0
        disable         # 日志显示输出
    """
    import logging

    logging.basicConfig(filename=filename,
                        filemode=filemode,
                        format='%(asctime)s  %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=level
                        )
    logging.disable = disable
    logging.warning(logs)
