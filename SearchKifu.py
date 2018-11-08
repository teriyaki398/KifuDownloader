# coding: utf-8

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

# 操作するブラウザの準備
option = webdriver.ChromeOptions()
option.add_argument('--headless')
driver = webdriver.Chrome(executable_path='./chromedriver', options=option)

url = 'http://swks.sakura.ne.jp/wars/kifusearch/'
u_name = 'T3RRY'

driver.get(url)

driver.find_element_by_id('id_name1').send_keys(u_name)
driver.find_element_by_id('searchBtn').click()

# ページのソースを取得
soup = BeautifulSoup(driver.page_source, 'lxml')
driver.quit()

lis = soup.find_all(class_='btn1')
kif = []

for i in lis:
    if 'kif' in i.get('href'):
        kif.append(i.get('href'))

kif = ['http://swks.sakura.ne.jp/wars' + x[2:] for x in kif]

for i in tqdm(kif):
    r = requests.get(i)
    r.encoding = 'Shift_JIS'

    f_name = i.split('/')[-1]
    # ユーザ名のディレクトリ以下にファイルを保存するようにしている
    # あらかじめディレクトリを作成しておく
    with open(u_name + '/' + f_name, mode='w') as f:
        f.write(r.text)
