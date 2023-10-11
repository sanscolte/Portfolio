from requests import ReadTimeout
from backoff import on_exception, expo
from requests.exceptions import ConnectTimeout
from typing import Dict
import requests
import os


def api_request(method_endswith: str,
                method_type: str,
                payload: Dict[str, int] = None,
                params: Dict = None):
    """
    Функция запроса данных от пользователя

    :param method_endswith: конец ссылки endpoint после '.com/'
    :type method_endswith: str
    :param method_type: тип запроса
    :type method_type: str
    :param payload: словарь с данными запроса
    :type payload: dict
    :param params: параметры запроса
    :type params: dict
    """

    url: str = f"https://hotels4.p.rapidapi.com/{method_endswith}"

    if method_type == 'GET':
        return get_request(
            url=url,
            params=params)
    else:
        return post_request(
            url=url,
            payload=payload)


@on_exception(wait_gen=expo, exception=(ReadTimeout, ConnectTimeout))
def get_request(url: str, params: Dict):
    """
    Функция запроса GET данных от API

    :param url: ссылка на endpoint
    :type url: str
    :param params: параметры запроса
    :type params: dict
    """

    headers: Dict[str] = {
        "X-RapidAPI-Key": os.getenv('KEY'),
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    try:
        response = requests.request(method="GET", url=url, headers=headers, params=params, timeout=15)

        if response.status_code == requests.codes.ok:
            return response
        else:
            return ReadTimeout

    except ReadTimeout:
        return ReadTimeout


@on_exception(wait_gen=expo, exception=(ReadTimeout, ConnectTimeout))
def post_request(url: str, payload: Dict[str, int]):
    """
    Функция запроса POST данных от API

    :param url: ссылка на endpoint
    :type url: str
    :param payload: словарь с данными запроса
    :type payload: dict
    """

    headers: Dict[str] = {
        "content-type": "application/json",
        "X-RapidAPI-Key": os.getenv('KEY'),
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    try:
        response = requests.request(method="POST", url=url, json=payload, headers=headers, timeout=15)

        if response.status_code == requests.codes.ok:
            return response
        else:
            raise ReadTimeout

    except (ReadTimeout, ConnectTimeout):
        raise ReadTimeout
