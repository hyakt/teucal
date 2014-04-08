#-*- coding: utf-8 -*-
import unicodedata
import re
from bs4 import BeautifulSoup


# 全角英数を半角英数に変換
def convertZenhan(html):
    s = html.read().decode('utf-8')
    html = unicodedata.normalize('NFKC', s).encode('utf-8')
    return html

html = open('plan.html', 'r')
soup = BeautifulSoup(convertZenhan(html))

f = open('test.html', 'w')

# 適宜変更
source = soup.find_all('table', border="1")

records = []
for tbody in source:
    for tr in tbody("tr"):
        tmplist = []
        for cnt, td in enumerate(tr.stripped_strings):
            if cnt == 1:
                print(td.encode('utf-8'))
                # print(re.findall(r'(\d+)月', td.encode('utf-8')))
                # print(re.findall(r'(\d+)日', td.encode('utf-8')))
                print(re.findall(r'(\d+)月(\d+|\s\d+)日', td.encode('utf-8')))

            if cnt == 0:
                # Subject,Start Date,All Day Event(True,False)
                tmplist.append(td.encode('utf-8'))
                # print(td.encode('utf-8'))
        records.append(tmplist)

# print records
