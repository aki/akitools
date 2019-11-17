# Copyright (c) 2019 aki


__version__ = '0.1.0'

__all__ = ['HEADER', 'ftime', 'ctime', 'mail', 'logs',
           'weather', 'ip', 'proxy', 'cryptocurrencies']


HEADER = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
          'Accept-Encoding': 'gzip, deflate, br',
          'Accept-Language': 'zh-CN,zh;q=0.9',
          'Cache-Control': 'max-age=0',
          'Connection': 'keep-alive',
          'Referer': None,
          'Sec-Fetch-Mode': 'navigate',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
          }


def ftime(t: int = None, f: int = None, c: str = None) -> str:
    """
    将时间戳转换成日期/时间字符串

        参数：
            t: 时间戳数字           # 默认值=当前时间的时间戳
            f: 已知的格式           # 默认值=1(可选1-5)
                                   # f=1 20140320
                                   # f=2 2014-03-20
                                   # f=3 2014/03/20
                                   # f=4 2014-03-20 10:28:24
                                   # f=5 2014/03/20 10:28:24
            c: 自定义格式           # 参考'%Y%m%d'格式,参数f与c为二选一，格式优先参数c的时间格式
        返回：
            return                  str
    """
    import time

    KNOWN_FORMATS = {
        1: '%Y%m%d',            # 20140320
        2: '%Y-%m-%d',          # 2014-03-20
        3: '%Y/%m/%d',          # 2014/03/20
        4: '%Y-%m-%d %H:%M:%S', # 2014-03-20 10:28:24
        5: '%Y/%m/%d %H:%M:%S', # 2014/03/20 10:28:24
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


def mail(recipient: list, subject: str, text: str) -> bool:
    """
    发送邮件

        参数：
            recipient           # 邮件收件人列表
            subject             # 邮件主题
            text                # 邮件内容
        返回:
            return              bool
    """
    from email.mime.text import MIMEText
    from email.header import Header
    import smtplib

    message = MIMEText(text, 'plain', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail("", recipient, message.as_string())
        return True
    except Exception as e:
        return False


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
            if ipaddr is None:
                raise
            if ipaddr != 'myip':
                re_text = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
                if re.match(re_text, ipaddr) is None:
                    raise
            return ipaddr

        def getInfo(ipaddr):
            ipaddr = handlerIp(ipaddr)
            data = {'ip': ipaddr}
            url = 'http://ip.taobao.com/service/getIpInfo2.php'
            response = requests.post(url, headers=HEADER, data=data, timeout=5)
            return response.json()

        data = getInfo(ipaddr)['data']
        data['timestamp'] = ctime()

        result['status'] = 'succeed'
        result['data'] = data
    except:
        result['status'] = 'fail'
        result['data'] = None
    finally:
        return result


###############################################################################################
__proxys = []


def __load_proxys():
    """加载代理数据"""
    import requests

    try:
        url = 'http://118.24.52.95/get_all/'
        response = requests.get(url, headers=HEADER)
        rest = response.json()
        for i in rest:
            __proxys.append(i['proxy'])
    except:
        pass


def proxy(n: int = 1) -> dict:
    """
    获取代理IP信息

        参数:
            n                   # 获取个数，默认 1个
        返回:
            return              dict
    """
    result = {}
    datas = []

    try:
        n = n if isinstance(n, int) else 1

        if len(__proxys) < n:
            __load_proxys()

        for i in range(n):
            data = {'proxy': __proxys.pop()}
            data['timestamp'] = ctime()
            datas.append(data)

        result['status'] = 'succeed'
        result['data'] = datas
    except:
        result['status'] = 'fail'
        result['data'] = None
    finally:
        return result

###############################################################################################


def cryptocurrencies(urrency: str = 'btcusd') -> dict:
    """
    获取加货币牌价
        参数:

            urrency             # 货币符号  btcusd, btceur, eurusd, xrpusd, xrpeur, xrpbtc, ltcusd, ltceur, ltcbtc,
                                #          ethusd, etheur, ethbtc, bchusd, bcheur, bchbtc
        返回:
            return              dict
    """
    import requests

    result = {}

    try:
        api_url = 'https://www.bitstamp.net/api/v2/ticker/{}/'.format(urrency)
        response = requests.get(api_url, headers=HEADER)
        data = response.json()

        result['status'] = 'succeed'
        result['data'] = data
    except:
        result['status'] = 'fail'
        result['data'] = None
    finally:
        return result
