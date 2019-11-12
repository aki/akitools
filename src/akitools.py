# Copyright (c) 2019 aki


__all__ = ['HEADER', 'ftime', 'ctime', 'send_mail', 'log_write']

__version__ = '0.0.21'


HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}


def ftime(t: int=None, f: int=None, c: str=None) -> str:
    """
    将时间戳转换成日期/时间字符串
        参数：
            t: 时间戳数字               # 默认值=当前时间的时间戳
            f: 已知的格式               # 默认值=1(可选1-5)
            c: 自定义格式               # 参考'%Y%m%d'格式,参数f与c为二选一，格式优先参数c的时间格式

            以下是提供常用的格式(参数f):
            f=1 20140320
            f=2 2014-03-20
            f=3 2014/03/20
            f=4 2014-03-20 10:28:24
            f=5 2014/03/20 10:28:24
        返回：
            return str
    """
    import time

    KNOWN_FORMATS = {
        1: '%Y%m%d',                    # 20140320
        2: '%Y-%m-%d',                  # 2014-03-20
        3: '%Y/%m/%d',                  # 2014/03/20
        4: '%Y-%m-%d %H:%M:%S',         # 2014-03-20 10:28:24
        5: '%Y/%m/%d %H:%M:%S',         # 2014/03/20 10:28:24
    }

    t = t if t else time.time()
    if c:
        return time.strftime(c, time.localtime(t))
    return time.strftime(KNOWN_FORMATS.get(f, KNOWN_FORMATS[1]), time.localtime(t))


def ctime(d: str=None) -> int:
    """
    将日期/时间字符串转换成时间戳
        参数：
            d:  日期/时间字符串         # 值为空返回当前时间的时间戳
        返回：
            return int            
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
