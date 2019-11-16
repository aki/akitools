# Copyright (c) 2019 aki

__all__ = ['HEADER', 'ftime', 'ctime', 'mail', 'logs', 'weather', 'ip']

__version__ = '0.0.24'


HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}


def ftime(t: int = None, f: int = None, c: str = None) -> str:
    """
    将时间戳转换成日期/时间字符串

        参数：
            t: 时间戳数字           # 默认值=当前时间的时间戳
            f: 已知的格式           # 默认值=1(可选1-5)
            c: 自定义格式           # 参考'%Y%m%d'格式,参数f与c为二选一，格式优先参数c的时间格式

            以下是提供常用的格式(参数f):
            f=1 20140320
            f=2 2014-03-20
            f=3 2014/03/20
            f=4 2014-03-20 10:28:24
            f=5 2014/03/20 10:28:24
        返回：
            return                  str
    """
    import time

    KNOWN_FORMATS = {
        1: '%Y%m%d',  # 20140320
        2: '%Y-%m-%d',  # 2014-03-20
        3: '%Y/%m/%d',  # 2014/03/20
        4: '%Y-%m-%d %H:%M:%S',  # 2014-03-20 10:28:24
        5: '%Y/%m/%d %H:%M:%S',  # 2014/03/20 10:28:24
    }

    t = t if t else time.time()
    if not c:
        c = KNOWN_FORMATS.get(f, KNOWN_FORMATS[1])
    return time.strftime(c, time.localtime(t))


def ctime(d: str = None) -> int:
    """
    将日期/时间字符串转换成时间戳

        参数：
            d:                  # 日期/时间字符串,值为空默认返回当前时间的时间戳
        返回：
            return              int            
    """
    import time
    from dateutil.parser import parse

    if d:
        return int(parse(d).timestamp())
    return int(time.time())


def mail(recipient: list, subject: str, text: str):
    """
    发送邮件

        参数：
            recipient           # 邮件收件人列表
            subject             # 邮件主题
            text                # 邮件内容
        返回:
            return              None
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


def logs(filename: str, log: str, filemode: str = 'a', level: int = 30, disable: bool = False):
    """
    日志写入

        参数:
            filename            # 日志文件名
            logs                # 日志内容
            filemode            # 写入模式      a w
            level               # 日志模式      CRITICAL=50 FATAL=50 ERROR=40 WARNING=30 WARN=30 INFO=20 DEBUG= 0 NOTSET=0
            disable             # 日志显示输出
        返回:
            return              None
    """
    import logging

    logging.basicConfig(filename=filename,
                        filemode=filemode,
                        format='%(asctime)s  %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=level)
    logging.disable = disable
    logging.warning(log)


def weather(city: str = None, version: int = 1) -> dict:
    """
    获取实时气象情况

        参数：
            city                # 城市名称  默认值为当前IP所在的城市
            version             # 数据版本  默认版本为1
        返回：
            return              dict
    """
    import requests
    import re
    import json
    from urllib import parse

    result = {}

    try:

        def request(url):
            """url请求"""
            header = HEADER
            header['Referer'] = url
            response = requests.get(url, headers=header, timeout=5)
            return response

        def default_city():
            """默认城市"""
            url = 'http://wgeo.weather.com.cn/ip/'
            rst = request(url)
            re_text = r'var id="(.*?)";var'
            re_result = re.findall(re_text, rst.text)
            return re_result[0]

        def search_cityname(cityname):
            """搜索城市代号"""
            ref = []
            cityname = parse.quote(cityname)
            url = 'http://toy1.weather.com.cn/search?cityname={}'
            url = url.format(cityname)
            rst = request(url)
            rst = re.sub(r"[()]", '', rst.text)
            rst = json.loads(rst)
            for i in rst:
                text = i['ref'].split('~')
                ref.append([text[0], text[2], text[-1]])
            return ref

        def _weather(city, version):
            """获取气象信息"""
            city = city if city else default_city()
            if not isinstance(city, int):
                city = search_cityname(city)[0][0]

            if version == 1:
                url = 'http://d1.weather.com.cn/dingzhi/{}.html'
                re_text = re.compile(r'weatherinfo":(.*?)};var')
            else:
                url = 'http://d1.weather.com.cn/sk_2d/{}.html'
                re_text = re.compile(r'= (.*?})')

            url = url.format(city)
            rst = request(url)
            rst = rst.text.encode(rst.encoding).decode(rst.apparent_encoding)
            rst = re.sub(r"[℃]", '', rst)
            re_result = re.findall(re_text, rst)
            resrstult = json.loads(re_result[0])
            resrstult['timestamp'] = ctime()
            return resrstult

        result['status'] = 'succeed'
        result['data'] = _weather(city, version)
    except:
        result['status'] = 'fail'
        result['data'] = None
    finally:
        return result


def ip(ipaddr: str = 'myip') -> dict:
    """
    获取ip地址信息

        参数:
            ipaddr              # ip地址 默认为本机ip地址
        返回:
            return              dict
    """
    import requests
    import re

    result = {}

    try:

        def handlerIp(ipaddr):
            if ipaddr and ipaddr != 'myip':
                re_text = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
            if re.match(re_text, ipaddr) is None or ipaddr is None:
                raise
            return ipaddr

        ipaddr = handlerIp(ipaddr)
        data = {'ip': ipaddr}
        url = 'http://ip.taobao.com/service/getIpInfo2.php'
        response = requests.post(url, headers=HEADER, data=data, timeout=5)
        resp = response.json()

        result['status'] = 'succeed'
        result['data'] = resp['data']
    except:
        result['status'] = 'fail'
        result['data'] = None
    finally:
        return result
