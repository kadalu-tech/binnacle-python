from binnacle.core import *

import urllib3

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


def post(url, status = 200):
    task = Task.from_frameinfo()
    try:
        resp = requests.get(full_url(url), headers=_headers)
        task.ok = resp.status_code == status
    except urllib3.exceptions.NewConnectionError:
        pass
    summary.add_completed_task(task)
    return resp


def put(url, status = 200):
    task = Task.from_frameinfo()
    try:
        resp = requests.get(full_url(url), headers=_headers)
        task.ok = resp.status_code == status
    except urllib3.exceptions.NewConnectionError:
        pass
    summary.add_completed_task(task)
    return resp


def get(url, status = 200):
    task = Task.from_frameinfo()
    try:
        resp = requests.get(full_url(url), headers=_headers)
        task.debug(f"URL: GET {url}\nExpected Status: {status}\nActual Status: {resp.status_code}")
        task.ok = resp.status_code == status
    except urllib3.exceptions.NewConnectionError:
        pass
    summary.add_completed_task(task)
    return resp.text


def delete(url, status = 204):
    task = Task.from_frameinfo()
    try:
        resp = requests.get(full_url(url), headers=_headers)
        task.ok = resp.status_code == status
    except urllib3.exceptions.NewConnectionError:
        pass
    summary.add_completed_task(task)
    return resp


def validated_json(data):
    task = Task.from_frameinfo()
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

    summary.add_completed_task(task)
    return jsondata


