#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, requests
from typing import Dict
from requests import Response
from datetime import datetime
from hashlib import md5
from urllib.parse import urlencode


class JDClient:
    """
    京东联盟 API SDK
    """

    def __init__(self, app_key: str, app_secret: str) -> None:
        """
        :param app_key: 京东联盟 APP KEY
        :param app_secret: 京东联盟 APP SECRET
        """
        self.endpoint = 'https://api.jd.com/routerjson'     # API服务的URL地址
        self.app_key = app_key
        self.app_secret = app_secret

    def __get_system_params(self, method: str) -> Dict:
        """
        系统参数构造函数
        :param method: API接口名称
        :return: 系统参数
        """

        return {
            'method': method,
            'app_key': self.app_key,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'format': 'json',
            'v': '1.0',
            'sign_method': 'md5'
        }

    def __get_business_params(self, params: Dict) -> Dict:
        """
        业务参数构造函数
        :param params: 业务参数
        :return: 业务参数
        """

        return {'360buy_param_json': json.dumps(params, ensure_ascii=False)}

    def __get_sign(self, params: Dict) -> str:
        """
        获取API输入参数签名
        :param params: 系统参数 + 业务参数
        :return: 签名结果
        """

        sign_str = ''
        for key in sorted(params):
            sign_str += key + params[key]
        sign_str = self.app_secret + sign_str + self.app_secret

        return md5(sign_str.encode()).hexdigest().upper()

    def request(self, method: str, params: Dict) -> Response:
        """
        发起请求
        :param method: API接口名称
        :param params: 业务参数
        :return: API返回结果
        """

        system_params = self.__get_system_params(method)
        business_params = self.__get_business_params(params)
        req_params = {**system_params, **business_params}

        sign = self.__get_sign(req_params)
        req_params['sign'] = sign

        response = requests.get(self.endpoint, params=urlencode(req_params))
        return response


if __name__ == '__main__':
    client = JDClient('app_key', 'app_secret')
    result = client.request(
        method='jd.union.open.category.goods.get',
        params={'goodsReqDTO': {'keyword': '鞋', 'pageIndex': 1}}
    )
    print(result.json())
