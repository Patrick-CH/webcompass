import datetime
import os

import requests
import re
import json
from urllib.parse import urlencode

cookies = {
    'lhct_1401462591_1207014257_cmsck': '15',
    'lhct_1401462591_1452035482_cmsck': '15',
    'CLIENT_IP': '119.79.240.223',
    'EDUWEBDEVICE': '4aba508aa2ea4fdf81c1b416a5f14922',
    'MOOC_PRIVACY_INFO_APPROVED': 'true',
    '__utma': '63145271.1839596308.1574766588.1576142298.1576142298.27',
    '__yadk_uid': 'Gq8BcT98sZ9z4GUH0X4ATXt33lPCbVBd',
    'P_INFO': 'chen__yuke@163.com|1584525518|1|imooc|00&99|hub&1584525496&imooc#hub&420100#10#0#0|&0|imooc'
              '|chen__yuke@163.com',
    'videoResolutionType': '2',
    'hasVolume': 'true',
    'videoRate': '1.5',
    'videoVolume': '1',
    'NTESSTUDYSI': '1d0acedb1b7d48228fb92db14419053d',
    'STUDY_INFO': 'oP4xHuLydWTsTiL3UAbvMOnMy4OE|6|1401462591|1606966447369',
    'STUDY_SESS': '"NET6igtCD6+IA2RyFj/ROfgz1zMY2G1bef9+3a/cW8KJVWvvU7qkJd7NDcWHXP8gd'
                  '+mzFdPP6F26gSgKDRiWgCZG9155GIT+f8yo7IU6UZEuJiCeyLAfB/DH63FGXSmSgfj9ZfTi3xc5CSQDPi1EpOh9h7vVVU'
                  '+Zk9HLRbMZiqcLhur2Nm2wEb9HcEikV+3FTI8+lZKyHhiycNQo+g+/oA=="',
    'STUDY_PERSIST': '"ezEXbV+SwkHcqutLRmfzpSULP0LV5Y6cE+E7LBb12tUZw/NVUTmd9b2ynyGc36iV1Q4zqLR1nBOKeHNLlXHL2iedRj'
                     '/cmDL8PIwUsSgA58AIHgzAZyH1d'
                     '/isnbVpZNtBr8K6RG5TZ4Nz7Z6BBxMAgsPiCuXgSSBBqoNoNqjM9dl7br3qdouGb2NclX8vH0jpVx5B2a'
                     '+GIBwRFNX9S2PNWwLG8fp0SzFWjYfKChAOdpvZgpjCC7Iso4RP9U87vJE8LtaQzUT1ovP2MqtW5+L3Hw+PvH8'
                     '+tZRDonbf7gEH7JU="',
    'NETEASE_WDA_UID': '1401462591#|#1569294669034',
    'Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b': '1606639047,1606826083,1606828855,1606966447',
    'WM_NI': '2A%2F4b2ao8k9FfQ%2Ft914MDXN9cX51jEz7f%2BE0tkdNNn%2F4rcIMli2uyHFGfX0ACToEVZFWE606GGHi9MhJItk0FG'
             '%2Bc8S67QoHg8EZ5LJKgpLVgcfIXig0U55eHnZ2GXXeQdlY%3D',
    'WM_NIKE': '9ca17ae2e6ffcda170e2e6ee99f15a97938ab9b659b6b48ba2c84f838f9abbaa4597b4c09bdc649888fa97fb2af0fea7c3b92af29fe1d5e13aa3b1f88cbc4ea68fe195bc3bf8938cb9cd33a188fbd2e94fbae9aaccc83cb8b5acafcd66edecbe84cc47b0b7fe96fc448699aab9b34b818ca1a6d55286898bd7b33e8599888abc47ac968795ea3c8699e584bb59f6e99f90cb6dfc9b96d6cf4289b9c0add56da1ba87b9ec6df48bfbd6e844ae86fea8db54a78fac8ddc37e2a3',
    'WM_TID': 'nCl98ICmWPJABQAVEEJ87dl6aC9OG4Vs',
    'Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b': '1606966568'
}
DOWNLOAD_PATH = 'D:\\Download\\'


def get_vid(url):
    url_id = url.split('#')[0]
    headers_id = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) \
    Chrome / 87.0.4280.66Safari / 537.36',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1'
    }
    r_id = requests.get(url_id, headers=headers_id)
    pattern = re.compile('"videoId": (.*?),')
    text = r_id.text
    ls = re.findall(pattern, text)
    print(ls[0])
    return ls[0]


def get_info():
    headers_sn = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '40',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'EDUWEBDEVICE=4aba508aa2ea4fdf81c1b416a5f14922; MOOC_PRIVACY_INFO_APPROVED=true; '
                  '__utma=63145271.1839596308.1574766588.1576142298.1576142298.27; '
                  '__yadk_uid=Gq8BcT98sZ9z4GUH0X4ATXt33lPCbVBd; '
                  'P_INFO=chen__yuke@163.com|1584525518|1|imooc|00&99|hub&1584525496&imooc#hub&420100#10#0#0|&0|imooc'
                  '|chen__yuke@163.com; videoResolutionType=2; hasVolume=true; videoRate=1.5; videoVolume=1; '
                  'WM_NI=2A%2F4b2ao8k9FfQ%2Ft914MDXN9cX51jEz7f%2BE0tkdNNn%2F4rcIMli2uyHFGfX0ACToEVZFWE606GGHi9MhJItk0FG'
                  '%2Bc8S67QoHg8EZ5LJKgpLVgcfIXig0U55eHnZ2GXXeQdlY%3D; '
                  'WM_NIKE'
                  '=9ca17ae2e6ffcda170e2e6ee99f15a97938ab9b659b6b48ba2c84f838f9abbaa4597b4c09bdc649888fa97fb2af0fea7c3b'
                  '92af29fe1d5e13aa3b1f88cbc4ea68fe195bc3bf8938cb9cd33a188fbd2e94fbae9aaccc83cb8b5acafcd66edecbe84cc47b'
                  '0b7fe96fc448699aab9b34b818ca1a6d55286898bd7b33e8599888abc47ac968795ea3c8699e584bb59f6e99f90cb6dfc9b9'
                  '6d6cf4289b9c0add56da1ba87b9ec6df48bfbd6e844ae86fea8db54a78fac8ddc37e2a3; WM_TID=nCl98ICmWPJABQAVEEJ8'
                  '7dl6aC9OG4Vs; NTESSTUDYSI=6fc510c409dc402eb9c3d0022c63a51e; '
                  'STUDY_INFO=oP4xHuLydWTsTiL3UAbvMOnMy4OE|6|1401462591|1606970098514; '
                  'STUDY_SESS="NET6igtCD6+IA2RyFj/ROfgz1zMY2G1bef9+3a/cW8KJVWvvU7qkJd7NDcWHXP8gd'
                  '+mzFdPP6F26gSgKDRiWgKYeAvnJUQdcvxiSOuMFA3DkOElsT3BWGz/l9WvPFy+ZVtGPdzD6mudmR10Ii0kWvswHSyQez3C'
                  '/kNVV1oL0C68Lhur2Nm2wEb9HcEikV+3FTI8+lZKyHhiycNQo+g+/oA=="; '
                  'STUDY_PERSIST="ezEXbV+SwkHcqutLRmfzpSULP0LV5Y6cE+E7LBb12tUZw'
                  '/NVUTmd9b2ynyGc36iV1Q4zqLR1nBOKeHNLlXHL2iedRj'
                  '/cmDL8PIwUsSgA58BnFrzisdBcngFymxORF8OmM0m2eAgU0c1Kk1B9FO6p5XZSQMVr2/dTycUJQiCVP1LnGQtPA2Ea7IU+Rg'
                  '+5lUc9AqZpar4dYrWNbzqlfWkXYKIvcZ+JfKxDFok20u79Y6/ZgpjCC7Iso4RP9U87vJE8LtaQzUT1ovP2MqtW5+L3Hw+PvH8'
                  '+tZRDonbf7gEH7JU="; NETEASE_WDA_UID=1401462591#|#1569294669034; '
                  'Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1606826083,1606828855,1606966447,1606970098; '
                  'Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1606971880',
        'origin': 'https://www.icourse163.org',
        'referer': 'https://www.icourse163.org/learn/ECNU-1206459847?tid=1461143452',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.66 Safari/537.36 '
    }
    # csrfKey = '6fc510c409dc402eb9c3d0022c63a51e'
    p = re.compile('NTESSTUDYSI=(\w+)')
    csrfKey = re.findall(p, headers_sn['cookie'])[0]
    print('csrfKey:' + csrfKey)
    url = 'https://www.icourse163.org/web/j/resourceRpcBean.getResourceToken.rpc?csrfKey={}'.format(csrfKey)
    data = {
        'bizId': '1257430794',
        'bizType': '1',
        'contentType': '1',
    }
    r = requests.post(url=url, data=data, headers=headers_sn, cookies=cookies)
    js_text = r.text
    d = json.loads(js_text)
    info = d.get('result').get('videoSignDto')
    videoId = str(info.get('videoId'))
    signature = info.get('signature')
    print('videoId = ' + videoId)
    print('signature = ' + signature)
    return videoId, signature


def get_video_url(video_id, signature):
    video_url_list = []
    headers_gv = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.66 Safari/537.36 '
    }
    param = {
        'videoId': video_id,
        'signature': signature,
        'clientType': 1
    }
    url = 'https://vod.study.163.com/eds/api/v1/vod/video?' + urlencode(param)
    # print(url)
    r = requests.get(url, headers=headers_gv)
    d = json.loads(r.text)
    for i in d.get('result').get('videos'):
        video_url_list.append(i.get('videoUrl'))
        # print(i.get('videoUrl'))
    return video_url_list


def m3u8(url, nowTime):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.98 Safari/537.36 '
    }
    # requests得到m3u8文件内容
    content = requests.get(url, headers=header).text
    if "#EXTM3U" not in content:
        print("这不是一个m3u8的视频链接！")
        return False
    # 得到每一个ts视频链接
    tslist = re.findall('EXTINF:(.*),\n(.*)\n#', content)
    newlist = []
    for i in tslist:
        newlist.append(i[1])

    # 先获取URL/后的后缀，再替换为空
    urlkey = url.split('/')[-1]
    url2 = url.replace(urlkey, '')  # 这里为得到url地址的前面部分，为后面key的链接和视频链接拼接使用

    # 得到每一个完整视频的链接地址
    tslisturl = []
    for i in newlist:
        tsurl = url2 + i
        tslisturl.append(tsurl)

    # for循环获取视频文件
    for i in tslisturl:
        res = requests.get(i, header)
        # 以追加的形式保存为mp4文件
        with open(DOWNLOAD_PATH + nowTime + '.mp4', 'ab+') as f:
            f.write(res.content)
    return True


def download_video(url):
    # url = 'https://www.icourse163.org/learn/ECNU-1003718005?tid=1450215443#/learn/content?type=detail&id=1214390655' \
    #       '&cid=1218061068 '
    info = get_info()
    videoId = info[0]
    signature = info[1]
    video_url_list = get_video_url(videoId, signature)
    nowTime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    for i in video_url_list:
        m3u8(i, nowTime)
    return DOWNLOAD_PATH + nowTime + '.mp4'
