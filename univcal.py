# -*- coding: utf-8 -*-
import unicodedata
import re
import csv
import ssl
from urllib import request
from datetime import date
from bs4 import BeautifulSoup

# 大学のURL
url = 'https://www.teu.ac.jp/inside/office/kyomu/953/20150301090000000000.html'
# url = "https://www.teu.ac.jp/inside/office/kyomu/953/scheduleH26_hachi.html"


# 大学の予定ページからhtmlを取得
def getUnivCal():
    https_sslv3_handler = request.HTTPSHandler(
        context=ssl.SSLContext(ssl.PROTOCOL_SSLv23))
    opener = request.build_opener(https_sslv3_handler)
    request.install_opener(opener)
    resp = opener.open(url)
    html = resp.read().decode('utf-8')
    # 全角英数字を半角英数字に変換
    html = unicodedata.normalize('NFKC', html)
    return html

# htmlの処理、記録
def soupUnivCal(html):
    year = date.today().strftime('%y')
    nyear = str(int(year) + 1)
    records = [['Subject', 'Start Date', 'End Date', 'All Day Event']]

    soup = BeautifulSoup(html)
    # 適宜変更
    src = soup.find_all('table', border="1")

    for tbody in src:
        for tr in tbody("tr"):
            tmplist = []
            for cnt, td in enumerate(tr.stripped_strings):
                if cnt == 1:
                    days = re.findall(r'(\d+)月(\d+|\s\d+)日', td)
                    daycnt = len(days)
                    # １月になったら翌年にする
                    if daycnt != 0:
                        if int(days[0][0]) == 1:
                            year = nyear
                    if daycnt == 1:
                        srtdate = days[
                            0][0] + '/' + days[0][1].strip() + '/' + year
                        tmplist.extend(
                            [srtdate, '', 'True'])
                    elif daycnt == 2:
                        srtdate = days[
                            0][0] + '/' + days[0][1].strip() + '/' + year
                        enddate = days[
                            1][0] + '/' + days[1][1].strip() + '/' + year
                        tmplist.extend(
                            [srtdate, enddate, 'True'])
                if cnt == 0:
                    tmplist.insert(0, td)
            records.append(tmplist)
    return records


# csvの書き込み
def writeCSV(csvlist):
    with open('gcal.csv', 'w') as f:
        csvWriter = csv.writer(f)
        for x in csvlist:
            if len(x) > 1:
                csvWriter.writerow(x)
                print(x)


# メイン関数
def main():
    html = getUnivCal()
    csvlist = soupUnivCal(html)
    writeCSV(csvlist)


if __name__ == '__main__':
    main()
