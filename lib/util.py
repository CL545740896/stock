#coding=utf-8
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def disable_requests_warn():
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)