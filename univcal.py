# -*- coding: utf-8 -*-
import unicodedata
import re
import csv
from urllib import request
from datetime import date
from bs4 import BeautifulSoup

# this year
tyear = date.today().strftime('%y')
nyear = str(int(tyear) + 1)
# csv output list
records = []
records.append(['Subject', 'Start Date', 'End Date', 'All Day Event'])
# next year flag
nyearflag = False
# url
url = 'https://www.teu.ac.jp/inside/office/kyomu/953/022096.html'


# 全角英数を半角英数に変換
def convertZenhan(html):
    s = html.read()
    html = unicodedata.normalize('NFKC', s)
    return html


def openUnivcal():
    with open('plan.html', encoding='utf-8') as html:
        soup = BeautifulSoup(convertZenhan(html))
        # 適宜変更
        source = soup.find_all('table', border="1")
        return source

if __name__ == '__main__':
    for tbody in openUnivcal():
        for tr in tbody("tr"):
            tmplist = []
            for cnt, td in enumerate(tr.stripped_strings):
                if cnt == 1:
                    days = re.findall(r'(\d+)月(\d+|\s\d+)日', td)
                    daycnt = len(days)
                    if daycnt != 0:
                        if int(days[0][0]) == 1:
                            nyearflag = True
                    if nyearflag:
                        if daycnt == 1:
                            srtdate = days[
                                0][0] + '/' + days[0][1].strip() + '/' + nyear
                            tmplist.extend(
                                [srtdate, '', 'True'])
                        elif daycnt == 2:
                            srtdate = days[
                                0][0] + '/' + days[0][1].strip() + '/' + nyear
                            enddate = days[
                                1][0] + '/' + days[1][1].strip() + '/' + nyear
                            tmplist.extend(
                                [srtdate, enddate, 'True'])
                    else:
                        if daycnt == 1:
                            srtdate = days[
                                0][0] + '/' + days[0][1].strip() + '/' + tyear
                            tmplist.extend(
                                [srtdate, '', 'True'])
                        elif daycnt == 2:
                            srtdate = days[
                                0][0] + '/' + days[0][1].strip() + '/' + tyear
                            enddate = days[
                                1][0] + '/' + days[1][1].strip() + '/' + tyear
                            tmplist.extend(
                                [srtdate, enddate, 'True'])
                if cnt == 0:
                    tmplist.insert(0, td)
            records.append(tmplist)

    with open('data.csv', 'w') as f:
        csvWriter = csv.writer(f)
        for x in records:
            if len(x) > 1:
                csvWriter.writerow(x)
                print(x)
