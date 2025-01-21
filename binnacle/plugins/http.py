import json

import requests

from binnacle.core import binnacle_task

_url = ""
_headers = {}

def base_url(url):
    global _url
    _url = url


def set_header(name, value):
    global _headers
    _headers[name] = f"{value}"


def remove_header(name):
    global _headers
    del _headers[name]


def headers(values):
    global _headers
    _headers = {}
    for name, value in values.items():
        _headers[name] = f"{value}"


def full_url(url):
    if url.startswith("http"):
        return url

    return _url + url


@binnacle_task
def http_post(url, status = 200, task=None):
    resp = requests.post(full_url(url), headers=_headers)
    task.ok = resp.status_code == status
    return resp


@binnacle_task
def http_put(url, status = 200, task=None):
    resp = requests.put(full_url(url), headers=_headers)
    task.ok = resp.status_code == status
    return resp


@binnacle_task
def http_get(url, status = 200, task=None):
    resp = requests.get(full_url(url), headers=_headers)
    task.debug(f"URL: GET {url}\nExpected Status: {status}\nActual Status: {resp.status_code}")
    task.ok = resp.status_code == status
    return resp.text


@binnacle_task
def http_delete(url, status = 204, task=None):
    resp = requests.delete(full_url(url), headers=_headers)
    task.ok = resp.status_code == status
    return resp


@binnacle_task
def validated_json(data, task=None):
    jsondata = {}

    try:
        jsondata = json.loads(data)
        task.ok = True
    except TypeError as ex:
        task.info(f"Invalid input data {ex}:\nData:\n{data}")
        task.ok = False
    except json.decoder.JSONDecodeError as ex:
        task.info(f"Invalid JSON {ex}:\nData:\n{data}")
        task.ok = False

    return jsondata


