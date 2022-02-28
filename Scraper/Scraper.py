from posixpath import split
from time import sleep
from turtle import title
from bs4 import BeautifulSoup
from numpy import double
import requests
import csv
import pandas as pd

req = requests.get("https://www.blockchain.com/btc/unconfirmed-transactions")
soup = BeautifulSoup(req.text, features="html.parser")
all = soup.find(class_ ="sc-1g6z4xm-0 hXyplo").text.strip().split()

listcoins = []
coin = []

for i in range(0,49):
    splitup = all[0].split('Time')

    hash = splitup[0]
    hash = hash.replace("Hash", "")
    time = splitup[1]
    time = time.replace("Amount", "")
    btc = all[1]
    btc = btc.replace("(BTC)", "")
    usd = all[3]
    usd = usd.replace("(USD)$", "")
    usd = usd.replace(",", " ")
    double(btc)
    double(usd)

    coin.append(hash)
    coin.append(time)
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