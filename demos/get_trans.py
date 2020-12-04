import requests
import json
from urllib.parse import urlencode


def GetTrans(language_from, language_to, content):
    if language_from == 'en' and content[-1] != '.':
        content += '.'
    url = 'http://fy.iciba.com/ajax.php?a=fy'
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/87.0.4280.66 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
               }
    body = '&f={}&t={}&w={}'.format(language_from, language_to, content)
    body = body.encode('utf-8')
    r = requests.post(url=url, data=body, headers=headers)
    # print(r.text)
    d = json.loads(r.text)
    print(d.get('content').get('out'))
    return d.get('content').get('out')