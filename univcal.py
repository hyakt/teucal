#-*- coding: utf-8 -*-
import unicodedata
from bs4 import BeautifulSoup

html = open('plan.html', 'r')
s = html.read().decode('utf-8')
html = unicodedata.normalize('NFKC', s).encode('utf-8')
soup = BeautifulSoup(html)

f = open('test.html', 'w')

# 適宜変更
source = soup.find_all('table', border="1")

for x in source:
    for y in x("tr"):
        print(y)


f.write(str(source))
