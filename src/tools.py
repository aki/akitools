
# 浏览器 User Agent
HEADER = {'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'}


def ftime(t: int = None, f: int = None, c: str = None) -> str:
    """将时间戳转换成日期/时间字符串

    :param t: 时间戳 （秒, 默认为当前的时间戳）
    :param f: 预先定义的格式 （默认选用 1）
    :param c: 自定义的格式
    :return str 日期

    预先定义的格式::

      f = 1 return 20140320
      f = 2 return 2014-03-20
      f = 3 return 2014/03/20
      f = 4 return 2014-03-20 10:28:24
      f = 5 return 2014/03/20 10:28:24
      f = 6 return 20140320102824

    """
    import time

    known_formats = {
        1: '%Y%m%d',  # 20140320
        2: '%Y-%m-%d',  # 2014-03-20
        3: '%Y/%m/%d',  # 2014/03/20
        4: '%Y-%m-%d %H:%M:%S',  # 2014-03-20 10:28:24
        5: '%Y/%m/%d %H:%M:%S',  # 2014/03/20 10:28:24
        6: '%Y%m%d%H%M%S',  # 20140320102824
    }

    t = t or time.time()
    c = c or known_formats.get(f, known_formats[1])
    return time.strftime(c, time.localtime(t))


def ctime(d: str = None) -> int:
    """将日期/时间字符串转换成时间戳

    :param d: 日期/时间字符串（默认为当前的时间）
    :return int 时间戳(秒)
    """
    import time
    from dateutil.parser import parse

    if d:
        return int(parse(d).timestamp())
    return int(time.time())


def filename_norm(f: str, s: str = "") -> str:
    """替换不符合文件名的字符

    :param f: 文件名字符串
    :param s: 替换后的字符 (1个字符)
    :return str
    """
    import re

    t = r'|/\\:*?"><'
    s = s if s not in t and len(s) <= 1 else ""
    f = re.sub('[{}]'.format(t), s, f)
    return f


def split_iterable(ls: list, n: int):
    """将可迭代的数据分割成多个列表

    :param ls: 可迭代的带下标的数据 (list, str)
    :param n: 每个列表数据的数量 (n>=1)
    :return list
    """
    from collections.abc import Iterable

    if isinstance(ls, Iterable) and isinstance(n, int) and n >= 1:
        result = [ls[i:i + n] for i in range(0, len(ls), n)]
        return result


def mail(recipient: list, subject: str, text: str) -> bool:
    """发送邮件

    :param recipient： 邮件收件人列表
    :param subject： 邮件主题
    :param text： 邮件内容
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
    except Exception as e:
        print(e)
        return False


def logs(filename: str, log: str, filemode: str = 'a', level: int = 30, disable: bool = False):
    """日志写入

    :param filename: 日志文件名
    :param log: 日志内容
    :param filemode: 写入模式
    :param level: 日志模式
    :param disable： 日志显示输出
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
    """获取实时气象情况 数据提供 weather.com.cn

    :param city: 城市名称
    :param version: 版本 (1 2 3)
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
            re_text = r'id="(\d+)'
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

        def _weather(c, v):
            """获取气象信息, c: city, v: version"""
            c = c if c else default_city()
            if not isinstance(c, int):
                c = search_city_name(c)[0][0]

            v = v if 1 <= v <= 3 else 1
            url = None
            re_text = None

            if v == 1:
                url = 'http://d1.weather.com.cn/dingzhi/{}.html'
                re_text = re.compile(r':({.*?})')
            elif v == 2:
                url = 'http://d1.weather.com.cn/sk_2d/{}.html'
                re_text = re.compile(r'({.*?})')
            elif v == 3:
                url = 'http://d1.weather.com.cn/weather_index/{}.html'
                re_text = re.compile(r'=*({.*?});')

            url = url.format(c)
            rst = request(url)
            rst = rst.text.encode(rst.encoding).decode(rst.apparent_encoding)
            rst = re.sub(r"[℃]", '', rst)
            re_result = re.findall(re_text, rst)
            if version == 3:
                rst = {i: d for i, d in enumerate(re_result)}
            else:
                rst = json.loads(re_result[0])
            rst['timestamp'] = ctime()
            return rst

        result['status'] = 'succeed'
        result['data'] = _weather(city, version)
    except Exception as e:
        result['status'] = str(e)
        result['data'] = None
    finally:
        return result


def ip_info(ip: str = 'myip') -> dict:
    """获取ip地址信息,数据提供方为 ip.taobao.com

    :param ip: ip地址
    :return dict
    """
    import requests
    import re

    result = {}

    try:
        if ip != 'myip':
            re_text = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
            if re.match(re_text, ip) is None:
                raise TypeError('IP地址有误: {}'.format(ip))

        data = {'ip': ip}
        url = 'http://ip.taobao.com/service/getIpInfo2.php'
        response = requests.post(url, headers=HEADER, data=data, timeout=5)

        data = response.json()['data']
        data['timestamp'] = ctime()

        result['status'] = 'succeed'
        result['data'] = data
    except Exception as e:
        result['status'] = str(e)
        result['data'] = None
    finally:
        return result
