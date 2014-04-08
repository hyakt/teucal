#-*- coding: utf-8 -*-
import unicodedata
from bs4 import BeautifulSoup


def convertZenhan(html):
    s = html.read().decode('utf-8')
    html = unicodedata.normalize('NFKC', s).encode('utf-8')
    return html

html = open('plan.html', 'r')
soup = BeautifulSoup(convertZenhan(html))

f = open('test.html', 'w')

# 適宜変更
source = soup.find_all('table', border="1")

for table in source:
    for tr in table("tr"):
        for cnt, td in enumerate(tr.stripped_strings):
            if cnt == 0:
                print(td.encode('utf-8'))
            if cnt == 1:
                print(td.encode('utf-8'))
