# Copyright (c) 2019 aki


__version__ = '0.1.3'

__all__ = ['HEADER', 'ftime', 'ctime', 'mail', 'logs', 'weather', 'ip']

# 浏览器 User Agent
HEADER = {'Accept': '*/*',
          'Accept-Encoding': 'gzip, deflate, br',
          'Accept-Language': 'zh-CN,zh;q=0.9',
          'Connection': 'keep-alive',
          'Referer': None,
          'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0',
          }


def ftime(timestamp: int = None, foregone: int = None, format: str = None) -> str:
    """将时间戳转换成日期/时间字符串

    :param timestamp 时间戳 （默认为当前的时间戳）
    :param foregone 预先定义的格式 （默认选用 1）
    :param format 自定义的格式
    :return str

    预先定义的格式::

      foregone = 1 return 20140320
      foregone = 2 return 2014-03-20
      foregone = 3 return 2014/03/20
      foregone = 4 return 2014-03-20 10:28:24
      foregone = 5 return 2014/03/20 10:28:24
    """
    import time

    KNOWN_FORMATS = {
        1: '%Y%m%d',  # 20140320
        2: '%Y-%m-%d',  # 2014-03-20
        3: '%Y/%m/%d',  # 2014/03/20
        4: '%Y-%m-%d %H:%M:%S',  # 2014-03-20 10:28:24
        5: '%Y/%m/%d %H:%M:%S',  # 2014/03/20 10:28:24
    }

    t = timestamp if timestamp else time.time()
    if not format:
        format = KNOWN_FORMATS.get(foregone, KNOWN_FORMATS[1])
    return time.strftime(format, time.localtime(t))


def ctime(datetime: str = None) -> int:
    """将日期/时间字符串转换成时间戳.

    :param datetime 日期/时间字符串（默认为当前的时间）
    :return timestamp
    """
    import time
    from dateutil.parser import parse

    if datetime:
        return int(parse(datetime).timestamp())
    return int(time.time())


def mail(recipient: list, subject: str, text: str) -> bool:
    """发送邮件

    :param recipient 邮件收件人列表
    :param subject 邮件主题
    :param text 邮件内容
    :return bool 发送成功为True, 否则为False
    """
    from email.mime.text import MIMEText
    from email.header import Header
    import smtplib

    message = MIMEText(text, 'plain', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtp_obj = smtplib.SMTP('localhost')
        smtp_obj.sendmail("", recipient, message.as_string())
        return True
    except:
        return False


def logs(filename: str, log: str, filemode: str = 'a', level: int = 30, disable: bool = False):
    """日志写入

    :param filename 日志文件名
    :param log 日志内容
    :param filemode 写入模式
    :param level 日志模式
    :param disable 日志显示输出
    :return None
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
    """获取实时气象情况

    :param city 城市名称
    :param version 版本 (1 or 2)
    :return dict
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

        def search_city_name(city_name):
            """搜索城市代号"""
            ref = []
            city_name = parse.quote(city_name)
            url = 'http://toy1.weather.com.cn/search?cityname={}'
            url = url.format(city_name)
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
                city = search_city_name(city)[0][0]

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
            result = json.loads(re_result[0])
            result['timestamp'] = ctime()
            return result

        result['status'] = 'succeed'
        result['data'] = _weather(city, version)
    except:
        result['status'] = 'fail'
        result['data'] = None
    finally:
        return result


def ip(ip_address: str = 'myip') -> dict:
    """获取ip地址信息,数据提供方为 ip.taobao.com

    :param ip_address ip地址
    :return dict
    """
    import requests
    import re

    result = {}

    try:
        def handlerIp(ip_address):
            if ip_address is None:
                raise
            if ip_address != 'myip':
                re_text = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
                if re.match(re_text, ip_address) is None:
                    raise
            return ip_address

        def getInfo(ip_address):
            ip_address = handlerIp(ip_address)
            data = {'ip': ip_address}
            url = 'http://ip.taobao.com/service/getIpInfo2.php'
            response = requests.post(url, headers=HEADER, data=data, timeout=5)
            return response.json()

        data = getInfo(ip_address)['data']
        data['timestamp'] = ctime()

        result['status'] = 'succeed'
        result['data'] = data
    except:
        result['status'] = 'fail'
        result['data'] = None
    finally:
        return result


def split_list(ls, num):
    """将列表分割成指定数量列表的多列表

    :param ls 源列表
    :param num 单个列表数据的数量
    :return list
    """

    from collections import Iterable
    if isinstance(ls, Iterable) and isinstance(num, int) and num >= 1:
        result = [ls[i:i + num] for i in range(0, len(ls), num)]
        return result
    return None