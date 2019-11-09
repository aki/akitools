# Copyright (c) 2019 aki


__all__ = ['version', 'ftime', 'ftimestamp', 'header', 'HEADER', 'send_mail', 'log_write']


version = '0.0.16'


HEADER = header()


def ftime(f: int = None, t: int = None, c: str = None) -> str:
    """
    将时间戳转换成指定的日期/时间格式
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


def ftimestamp(d: str, f: int = None, c: str = None) -> int:
    """
    将一个日期/时间转换成时间戳
        d:  日期/时间               # 2014-03-20
        f:  已知格式                # 为空则默认为 1
        c:  自定义格式              # 参考 '%Y%m%d' 格式
        如果参数f 与 c 都非空，则优先选择参数c 自定义的时间格式
            f = 1   =  '%Y%m%d'
            f = 2   =  '%Y.%m.%d'
            f = 3   =  2014-03-20
            f = 4   =  '%Y-%m-%d'
            f = 5   =  '%Y%m%d %H%M%S'
            f = 6   =  '%Y.%m.%d %H:%M:%S'
            f = 7   =  '%Y-%m-%d %H:%M:%S'
            f = 8   =  '%Y/%m/%d %H:%M:%S'
    """
    import time

    KNOWN_FORMATS = {
        1: '%Y%m%d',
        2: '%Y.%m.%d',
        3: '%Y-%m-%d',
        4: '%Y/%m/%d',
        5: '%Y%m%d %H%M%S',
        6: '%Y.%m.%d %H:%M:%S',
        7: '%Y-%m-%d %H:%M:%S',
        8: '%Y/%m/%d %H:%M:%S',
    }
    f = c if c else KNOWN_FORMATS.get(f, KNOWN_FORMATS[1])
    return int(time.mktime(time.strptime(d, f)))


def header() -> dict:
    """
    随机返回一个User-Agent,格式为字典
        {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'}
    """
    from random import choice

    KNOWN_LIST = ['Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
                  'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                  ]
    return {'User-Agent': choice(KNOWN_LIST)}


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
    # message['From'] = None
    # message['To'] = None
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail("", recipient, message.as_string())
    except Exception as e:
        print(e)


def log_write(filename: str, logs: str, filemode: str = 'a', level: int = 30, disable: bool = False):
    """
    日志记录
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
