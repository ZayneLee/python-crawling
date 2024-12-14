import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd

res = req.get("https://search.naver.com/search.naver?where=news&query=%EC%86%8D%EB%B3%B4&sm=tab_tmr&nso=so:r,p:all,a:all&sort=0")
soup = bs(res.text, "lxml")
title = soup.select("a.news_tit")
titleList = []
for i in title:
    titleList.append(i.text)

dic = {"뉴스제목" : titleList}
df = pd.DataFrame(dic)
df.to_csv("data2.csv", encoding="utf-8", index=False)
