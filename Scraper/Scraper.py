from posixpath import split
from sqlite3 import Time
import time
from turtle import title
from attr import attr
from bs4 import BeautifulSoup
from numpy import double
import requests
import csv
import pandas as pd

print("Enter 'ctrl + c' to stop the automated update")

while True:
    req = requests.get("https://www.blockchain.com/btc/unconfirmed-transactions")
    soup = BeautifulSoup(req.text, features="html.parser")
    all = soup.findAll('div' , attrs={'class' :"sc-1g6z4xm-0 hXyplo"})

    listcoins = []
    coin = []

    for i in range(0,49):
        tekst = all[i].text

        splitup = tekst.split('Time')

        hash = splitup[0]
        hash = hash.replace("Hash", "")
        Rest = splitup[1]
        Time = Rest[0:5]
        money = Rest[17:]
        splitup2 = money.split('BTCAmount')
        btc = splitup2[0]
        usd = splitup2[1]
        usd = usd.replace("(USD)$", "")
        usd = usd.replace(",", "")
        double(btc)
        double(usd)

        coin.append(hash)
        coin.append(Time)
        coin.append(btc)
        coin.append(usd)

        listcoins.append(coin)
        coin = []

    head = ['Hash', 'Time', 'BTC' , 'USD']
    with open('sorted.csv', 'w', encoding='UTF8') as filewrite:
        write = csv.writer(filewrite)
        write.writerow(head)
        write.writerows(listcoins)

    dataf = pd.read_csv("sorted.csv")
    dataf.sort_values(["BTC"], axis=0, ascending=[False], inplace=True)
    Firstfive = dataf.head(5)
    print(Firstfive)
    time.sleep(60)

    




