import zipfile
from time import time
from multiprocessing import Pool
import requests
import urllib
from pyquery import PyQuery as pq
import os
import re

download_path = 'D:\\ServerData\\pics\\'
file_list = list()


def get_page(keyword):
    html = ''
    # https://image.baidu.com/search/acjson?tn=resultjson_com&logid=11158509673023873269&ipn=rj&ct=201326592&is=&fp=result&queryWord=stmplib&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&word=stmplib&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&expermode=&force=&pn=30&rn=30&gsm=1e&1606738976153=
    urls = ['https://image.baidu.com/search/acjson?tn=resultjson_com&logid=7942992946129127376&ipn=rj&ct=201326592&is\
    =&fp=result&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word={}&s=&s\
    e=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn=60&rn=30&gsm=3c&{}='.format(
        keyword, keyword, str(time()).replace('.', '')[:-4]),
        'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=7942992946129127376&ipn=rj&ct=201326592&is=&fp=res\
    ult&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word={}&s=&se=&tab=&\
    width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn=30&rn=30&gsm=1e&{}='.format(
            keyword, keyword, str(time()).replace('.', '')[:-4])]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
               }
    for url in urls:
        try:
            r = requests.get(url=url, headers=headers)
            r.encoding = r.apparent_encoding
            if r.status_code == 200:
                html += r.text
            else:
                return None
        except requests.exceptions.ConnectionError:
            return None
    return html


def save_pics(url):
    global download_path
    path = download_path + url.split('/')[-1]
    try:
        if not os.path.exists(download_path):  # 判断根目录是否存在
            os.mkdir(download_path)  # 创建根目录
        if not os.path.exists(path):  # 判断文件是否存在
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                       'X - Requested - With': 'XMLHttpReques',
                       'Connection': 'keep - alive'
                       }  # 模拟浏览器访问
            r = requests.get(url, headers=headers)
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                # print(path + " is saved successfully")
                return path
        else:
            # print("file already exist")
            pass
    except os.error:
        print("vist failed")


def get_img_link(html):
    print("Getting the links...")
    img_link_list = list()
    matches = re.findall('"thumbURL":"(.*?)"', html)
    for matche in matches:
        img_link_list.append(matche)
    return img_link_list


def get_imgs(keyword):
    global file_list
    # 验证网络连接
    try:
        r = requests.get("https://www.baidu.com")
        if r.status_code != 200:
            print("You are not connected to the Internet!")
            exit(-1)
    except Exception:
        print("You are not connected to the Internet!")
        exit(-1)
    html = get_page(keyword)
    img_links = get_img_link(html)[0:50]
    print(len(img_links))
    pool = Pool()
    pool.map(save_pics, img_links)
    pool.close()
    pool.join()
    for img in img_links:
        path = download_path + img.split('/')[-1]
        file_list.append(path)
    zip_path = 'D:\\ServerData\\zips\\{}.zip'.format(str(time()).replace('.', ''))
    f = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    for i in file_list:
        f.write(i)
        # print(i)
    f.close()
    return zip_path


if __name__ == '__main__':
    start = time()
    print(get_imgs('makabaka'))
    end = time()
    print('time: ', end='')
    print(end - start)
