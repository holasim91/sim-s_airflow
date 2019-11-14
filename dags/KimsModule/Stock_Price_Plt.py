import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


class Stockprice:
    def __init__(self, code_num, start, end):
        self.code_num = code_num
        self.start = start
        self.end = end

    def stockprice(self):
        code_num = self.code_num
        url = "https://finance.naver.com/item/sise_day.nhn?code={}&page={}"
        df = pd.DataFrame()
        df["date"] = ""
        df["close"] = ""
        date_list = []
        close_list = []
        open_list = []
        high_list = []
        low_list = []
        volumn_list = []
        for i in range(1, 20):
            url_1 = url.format(code_num, i)
            resp = requests.get(url_1)
            soup = BeautifulSoup(resp.content, "html.parser")

            tr_tag = soup.find("table", class_="type2").find_all("tr")

            for i in tr_tag:
                try:
                    date = (
                        i.find("td", align="center")
                        .find("span", class_="tah p10 gray03")
                        .text
                    )
                    date_list.append(date)

                    td_tag = i.find_all("td", class_="num")

                    close = td_tag[0].text
                    close_list.append(close)

                    open_1 = td_tag[2].text
                    open_list.append(open_1)

                    high = td_tag[3].text
                    high_list.append(high)

                    low = td_tag[4].text
                    low_list.append(low)

                    volumn = td_tag[5].text
                    volumn_list.append(volumn)

                except:
                    pass

        df["date"] = date_list
        df["close"] = close_list
        df["open"] = open_list
        df["high"] = high_list
        df["low"] = low_list
        df["volumn"] = volumn_list

        close_price = df

        new_close_list = []
        new_high_list = []
        new_low_list = []
        new_volumn_list = []
        new_open_list = []

        for i in range(len(close_price)):
            new_close = float(close_price["close"][i].replace(",", ""))
            new_close_list.append(new_close)
        close_price["close2"] = new_close_list
        del close_price["close"]
        # self.close_price = close_price.rename(columns={'close2':'close'})

        for i in range(len(close_price)):
            new_open = float(close_price["open"][i].replace(",", ""))
            new_open_list.append(new_open)
        close_price["open2"] = new_open_list
        del close_price["open"]
        # self.close_price = close_price.rename(columns={'open2':'open'})

        for i in range(len(close_price)):
            new_high = float(close_price["high"][i].replace(",", ""))
            new_high_list.append(new_high)
        close_price["high2"] = new_high_list
        del close_price["high"]
        # self.close_price = close_price.rename(columns={'high2':'high'})

        for i in range(len(close_price)):
            new_low = float(close_price["low"][i].replace(",", ""))
            new_low_list.append(new_low)
        close_price["low2"] = new_low_list
        del close_price["low"]
        # self.close_price = close_price.rename(columns={'low2':'low'})

        for i in range(len(close_price)):
            new_volumn = float(close_price["volumn"][i].replace(",", ""))
            new_volumn_list.append(new_volumn)
        close_price["volumn2"] = new_volumn_list
        del close_price["volumn"]
        self.close_price = close_price.rename(
            columns={
                "volumn2": "volumn",
                "low2": "low",
                "open2": "open",
                "high2": "high",
                "close2": "close",
            }
        )
        return self.close_price

    def pltstock(self, datatype, style):
        # 주가 데이터 시각화
        close_price = self.close_price
        close_price["date"] = pd.to_datetime(close_price["date"])
        close_price = close_price.set_index("date")

        fig, ax = plt.subplots()
        fig.subplots_adjust(right=0.7)
        # close_plt = close_price[[datatype]].plot(ax=ax, style=style, figsize=(15,4))


#         fig, ax = plt.subplots()
#         fig.subplots_adjust(right=0.7)
#         open_plt = close_price[['open']].plot(ax=ax, style='r-', figsize=(15,4))

#         fig, ax = plt.subplots()
#         fig.subplots_adjust(right=0.7)
#         volumn_plt = close_price[['volumn']].plot(ax=ax, style='g-', figsize=(15,4))
