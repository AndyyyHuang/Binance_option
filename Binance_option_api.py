"""
# File         :Binance_option_api.py
# Time         :2022/3/25 13:58
# Author       :Andy
# contact      :2019200836@ruc.edu.cn
# version      :python 3.9
# Description:
"""

import requests
from urllib.parse import urljoin, urlencode
import hmac
import hashlib
import pandas as pd
import time

class BinanceException(Exception):

    def __init__(self, status_code, data):
        self.status_code = status_code
        if data:
            self.code = data['code']
            self.msg = data['msg']
        else:
            self.code = None
            self.msg = None
        message = f"{status_code} [{self.code}] {self.msg}"

        super().__init__(message)


class binance_option_api():
    """
    The European option api of binance
    You can see the official rest api documents of binance at :https://binance-docs.github.io/apidocs/voptions/en/#general-info
    """

    def __init__(self, api_key, api_secret, proxies):
        self.api_key = api_key
        self.api_secret = api_secret
        self.headers = {
            'X-MBX-APIKEY': api_key
        }
        self.proxies = proxies
        self.base_url = "https://vapi.binance.com"

    def get_option_info(self):
        """

        :return:
        """
        path = "/vapi/v1/optionInfo"
        url = urljoin(self.base_url, path)
        params = None
        r = requests.get(url=url, headers=self.headers, params=params, proxies=self.proxies)
        if r.status_code == 200:
            return r.json()['data']
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())

    def get_exchange_info(self):
        """

        :return:
        """
        path = "/vapi/v1/exchangeInfo"
        url = urljoin(self.base_url, path)
        params = None
        r = requests.get(url=url, headers=self.headers, params=params, proxies=self.proxies)
        if r.status_code == 200:
            return r.json()['data']
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())

    def get_spot_price(self, underlying: str):
        """

        :param underlying:
        :return:
        """
        path = "/vapi/v1/index"
        url = urljoin(self.base_url, path)
        params = {"underlying": underlying}
        r = requests.get(url=url, headers=self.headers, params=params, proxies=self.proxies)
        if r.status_code == 200:
            return r.json()['data']
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())

    def get_latest_24h_price(self, symbol: str):
        """

        :param symbol:
        :return:
        """
        path = "/vapi/v1/ticker"
        url = urljoin(self.base_url, path)
        params = {"symbol": symbol}
        r = requests.get(url=url, headers=self.headers, params=params, proxies=self.proxies)
        if r.status_code == 200:
            return r.json()['data']
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())

    def get_latest_24h_price(self, symbol: str):
        """

        :param symbol:
        :return:
        """
        path = "/vapi/v1/ticker"
        url = urljoin(self.base_url, path)
        params = {"symbol": symbol}
        r = requests.get(url=url, headers=self.headers, params=params, proxies=self.proxies)
        if r.status_code == 200:
            return r.json()['data']
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())

    def get_mark_price(self, symbol: str):
        """

        :param symbol:
        :return:
        """
        path = "/vapi/v1/mark"
        url = urljoin(self.base_url, path)
        params = {"symbol": symbol}
        r = requests.get(url=url, headers=self.headers, params=params, proxies=self.proxies)
        if r.status_code == 200:
            return r.json()['data']
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())

    def get_depth(self, symbol: str, limit: int=10):
        """

        :param symbol:
        :param limit:
        :return:
        """
        path = "/vapi/v1/depth"
        url = urljoin(self.base_url, path)
        params = {"symbol": symbol, "limit": limit}
        r = requests.get(url=url, headers=self.headers, params=params, proxies=self.proxies)
        if r.status_code == 200:
            return r.json()['data']
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())

    def get_k_line(self, symbol: str, interval: str, start_time: str, end_time: str, limit: int):
        """

        :param symbol:
        :param interval:
        :param start_time:
        :param end_time:
        :param limit:
        :return:
        """
        path = "/vapi/v1/klines"
        url = urljoin(self.base_url, path)
        params = {"symbol": symbol, 'interval': interval, 'startTime': start_time, 'endTime': end_time, "limit": limit}
        r = requests.get(url=url, headers=self.headers, params=params, proxies=self.proxies)
        if r.status_code == 200:
            return r.json()['data']
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())

    def get_latest_trades(self, symbol: str, limit: int):
        """

        :param symbol:
        :param limit:
        :return:
        """
        path = "/vapi/v1/trades"
        url = urljoin(self.base_url, path)
        params = {"symbol": symbol, "limit": limit}
        r = requests.get(url=url, headers=self.headers, params=params, proxies=self.proxies)
        if r.status_code == 200:
            return r.json()['data']
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())

    def make_single_order(self, **params):
        """

        :param params:
        :return:
        """
        path = "/vapi/v1/order"
        url = urljoin(self.base_url, path)
        query_string = urlencode(params)
        params['signature'] = hmac.new(self.api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        r = requests.get(url=url, headers=self.headers, params=params, proxies=self.proxies)
        if r.status_code == 200:
            return r.json()['data']
        else:
            raise BinanceException(status_code=r.status_code, data=r.json())

    def get_option_left_days(self, symbol: str):
        """

        :param symbol:
        :return:
        """
        temp = pd.DataFrame(self.get_option_info())
        expire = temp['expiryDate'].loc[temp.symbol == symbol].values[0] / 1000
        now = round(time.time())
        left_days = (expire - now) / (3600 * 24)

        return round(left_days, 3)
