import re
import time
import urllib
from urllib import parse

import requests
from py_mini_racer import MiniRacer


def initCTX():
    with open('getk.js', 'r', encoding='utf-8') as f:
        jsCode = f.read()
    ctx = MiniRacer()
    ctx.eval(jsCode)
    return ctx


def get_u(url):
    res = requests.get(url=url, headers={
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "zh-CN,zh;q=0.9",
        "referer": url,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }).text
    u = re.search(r'u:\{(?P<u>.*?),d:.*?},', res, re.S).group("u").strip().split(",")
    s = u[0].replace("\"", '')[2:]
    k = u[1].replace("\"", '')[2:]
    l = u[2].replace("\"", '')[2:]
    return s, k, l


def ios_search_word_app_rank(country_id, word, page):
    """ios搜索"""
    end_time = int(time.time())
    start_time = end_time - 2544942
    # 更新时间
    s, k, l = get_u(f"https://app.diandian.com/rank/monitor-1-1-{country_id}-{urllib.parse.quote(word)}")  # 替换加密参数
    k = CTX.call("ios_search_word_app_rank", country_id, word, page, s, k, l, end_time, start_time)
    # page页数， 一页有50条数据
    params = {
        "word": word,
        "market_id": "1",
        "device_id": "1",
        "country_id": str(country_id),
        "rank_type": "1",
        "order_by": "1",
        "rank_history": "",
        "app_name": "",
        "start_time": str(start_time),
        "end_time": str(end_time),
        "page": str(page),
        "k": k
    }
    res = requests.get('https://api.diandian.com/pc/app/v1/word/word_app_rank', headers={
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "api.diandian.com",
        "Origin": "https://app.diandian.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }, params=params).json()
    for i in res['data']['list']:
        # https://app.diandian.com/app/y53u5uw261kreu7/ios?market=1&country=75&id=1664702280
        print("id:", i['app']['id'])
        print("app_id:", i['app']['app_id'])
        print("market_id:", i['app']['market_id'])
        print("country_id:", i['app']['country_id'])
        print("软件名:", i['app']['name'])
        print("软件类型:", i['app']['title'])
        print("软件链接:",
              f"https://app.diandian.com/app/{i['app']['id']}/ios?market={i['app']['market_id']}&country={i['app']['country_id']}&id={i['app']['app_id']}")


def android_search_word_app_rank(country_id, word, page):
    """安卓搜索"""
    end_time = int(time.time())
    start_time = end_time - 2554897
    # 更新时间
    s, k, l = get_u(f"https://app.diandian.com/rank/monitor-11-1-{country_id}-{urllib.parse.quote(word)}")  # 替换加密参数
    k = CTX.call("android_search_word_app_rank", country_id, word, page, s, k, l, end_time, start_time)
    # page页数， 一页有50条数据
    params = {
        "word": str(word),
        "market_id": "11",
        "device_id": "1",
        "country_id": str(country_id),
        "rank_type": "1",
        "order_by": "1",
        "rank_history": "",
        "app_name": "",
        "start_time": str(start_time),
        "end_time": str(end_time),
        "page": str(page),
        "k": k
    }
    res = requests.get('https://api.diandian.com/pc/app/v1/word/word_app_rank', headers={
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Host": "api.diandian.com",
        "Origin": "https://app.diandian.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }, params=params).json()
    for i in res['data']['list']:
        # https://app.diandian.com/app/rn63ipuro9glcwn/googleplay?market=11&country=75&id=com.jisu.io
        print("id:", i['app']['id'])
        print("market_id:", i['app']['market_id'])
        print("country_id:", i['app']['country_id'])
        print("软件包名:", i['app']['bundle_id'])
        print("软件名:", i['app']['name'])
        print("软件类型:", i['app']['title'])
        print("软件链接:",
              f"https://app.diandian.com/app/{i['app']['id']}/googleplay?market={i['app']['market_id']}&country={i['app']['country_id']}&id={i['app']['bundle_id']}")


if __name__ == '__main__':
    CTX = initCTX()
    ios_search_word_app_rank(75, "字体", 1)  # 地区：75, 软件名："微信", 页数：1
    # android_search_word_app_rank(75, "淘宝", 1)
