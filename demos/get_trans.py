from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import wait
from urllib.parse import quote
from pyquery import PyQuery as pq


def get_translation(language_from, language_to, content):
    browser = webdriver.Chrome()
    waiter = wait.WebDriverWait(browser, 10)
    try:
        url = 'https://fanyi.baidu.com/?aldtype=16047#{}/{}/'.format(language_from, language_to) + quote(content)
        browser.get(url)
        waiter.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#main-outer > div > div > div.translate-wrap > \
            div.translateio > div.translate-main.clearfix > div.trans-right > div > div > div.output-bd > \
            p.ordinary-output.target-output.clearfix > span'))
        )
        browser.close()
        html = browser.page_source
        doc = pq(html)
        p = doc('#main-outer > div > div > div.translate-wrap > \
                div.translateio > div.translate-main.clearfix > div.trans-right > div > div > div.output-bd > \
                p.ordinary-output.target-output.clearfix > span')
        return p.text()
    except TimeoutException:
        print('Time out!')


if __name__ == '__main__':
    text = get_translation('zh', 'en', '你好')
    print(text)