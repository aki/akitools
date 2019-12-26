
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


def random_chinese_character(n: int = 3, surname: bool = True) -> str:
    """随机中文字符
    :param n: 数量
    :param surname: 姓氏
    :return str
    """
    from random import randint, choice

    """
    01李 02王 03张 04刘 05陈 06杨 07赵 08黄 09周 10吴
    11徐 12孙 13胡 14朱 15高 16林 17何 18郭 19马 20罗
    21梁 22宋 23郑 24谢 25韩 26唐 27冯 28于 29董 30萧
    31程 32曹 33袁 34邓 35许 36傅 37沈 38曾 39彭 40吕
    41苏 42卢 43蒋 44蔡 45贾 46丁 47魏 48薛 49叶 50阎
    51余 52潘 53杜 54戴 55夏 56钟 57汪 58田 59任 60姜
    61范 62方 63石 64姚 65谭 66廖 67邹 68熊 69金 70陆
    71郝 72孔 73白 74崔 75康 76毛 77邱 78秦 79江 80史
    81顾 82侯 83邵 84孟 85龙 86万 87段 88漕 89钱 90汤
    91尹 92黎 93易 94常 95武 96乔 97贺 98赖 99龚 100文
    """
    surnames = [0x674E, 0x738B, 0x5F20, 0x5218, 0x9648, 0x6768, 0x8D75, 0x9EC4, 0x5468, 0x5434,
                0x5F90, 0x5B59, 0x80E1, 0x6731, 0x9AD8, 0x6797, 0x4F55, 0x90ED, 0x9A6C, 0x7F57,
                0x6881, 0x5B8B, 0x90D1, 0x8C22, 0x97E9, 0x5510, 0x51AF, 0x51AF, 0x8463, 0x8427,
                0x7A0B, 0x66F9, 0x8881, 0x9093, 0x8BB8, 0x5085, 0x6C88, 0x66FE, 0x5F6D, 0x5415,
                0x82CF, 0x5362, 0x848B, 0x8521, 0x8D3E, 0x4E01, 0x9B4F, 0x859B, 0x53F6, 0x960E,
                0x4F59, 0x6F58, 0x675C, 0x6234, 0x590F, 0x949F, 0x6C6A, 0x7530, 0x4EFB, 0x59DC,
                0x8303, 0x65B9, 0x77F3, 0x59DA, 0x8C2D, 0x5ED6, 0x90B9, 0x718A, 0x91D1, 0x9646,
                0x90DD, 0x5B54, 0x767D, 0x5D14, 0x5EB7, 0x6BDB, 0x90B1, 0x79E6, 0x6C5F, 0x53F2,
                0x987E, 0x4FAF, 0x90B5, 0x5B5F, 0x9F99, 0x4E07, 0x6BB5, 0x6F15, 0x94B1, 0x6C64,
                0x5C39, 0x9ECE, 0x6613, 0x5E38, 0x6B66, 0x4E54, 0x8D3A, 0x8D56, 0x9F9A, 0x6587,
                ]

    unicode_min = 0x4E00
    unicode_max = 0x9FA5

    result = [chr(randint(unicode_min, unicode_max)) for _ in range(n)]
    if surname:
        result[0] = chr(choice(surnames))
        result = result[:3]
    return ''.join(result)


def random_password(n=10):
    """随机密码
    :param n: 密码位数
    :return:
    """
    from random import randint
    unicode_min = 0x0020
    unicode_max = 0x007E
    result = [chr(randint(unicode_min, unicode_max)) for _ in range(n)]
    return ''.join(result)


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
