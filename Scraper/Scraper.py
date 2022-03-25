from http import client
from posixpath import split
from sqlite3 import Time
import time
from attr import attr
from bs4 import BeautifulSoup
from numpy import double
import requests
import pickle
import csv
import pandas as pd
import pymongo
import redis

#connection to redis and mongodb
r = redis.Redis(host='localhost', port=6379)
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")

#make/know which db to use in mongodb
Scraperdatabase = client["BestfiveDB"]
mycol = Scraperdatabase["Bestfive"]

print("Enter 'ctrl + c' to stop the automated update")
loop = 0

#start loop to keep running the code
while True:
    #get acces to the site and return the div where the important data is stored
    req = requests.get("https://www.blockchain.com/btc/unconfirmed-transactions")
    soup = BeautifulSoup(req.text, features="html.parser")
    all = soup.findAll('div' , attrs={'class' :"sc-1g6z4xm-0 hXyplo"})

    #start a list to store the all 50 and a temporary list to put 1 into the big list of 50.
    listcoins = []
    coin = []

    #Loops 50 times and takes the HASH, Time, bitcoin quantity and USD quantity
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

        # Make a dictionary to put it in to redis
        tijdelijkerow = {'hash' : hash, 'time' : Time, 'BTC' : btc, 'USD' : usd}

        redis_dict = pickle.dumps(tijdelijkerow)
        r.set(f"fulldata{loop}", redis_dict)

        read_dict = r.get(f'fulldata{loop}')
        loop = loop + 1

        yourdict = pickle.loads(read_dict)
        coin = []
                
    
    #Make a csv with the 50 hashes, time, btc and usd.
    head = ['Hash', 'Time', 'BTC' , 'USD']
    with open('sorted.csv', 'w', encoding='UTF8') as filewrite:
        write = csv.writer(filewrite)
        write.writerow(head)
        write.writerows(listcoins)

    #Sort it on bitcoin from big to small and take the 5 biggest values
    dataf = pd.read_csv("sorted.csv")
    dataf = dataf.sort_values(["BTC"], ascending=[False])
   
    firstfive = dataf.head(5)
    print(firstfive)

    loop2 = 0

    #loop to take the 5 most valuable variables and put them in redis
    for i in range(0,5):
        tijdelijk = dataf.iloc[i]

        Hashbest = tijdelijk["Hash"]
        timebest = tijdelijk["Time"]
        btcbest = tijdelijk["BTC"]
        usdbest = tijdelijk["USD"]

        data = {'hash' : Hashbest, 'time' : timebest, 'BTC' : btcbest, 'USD' : usdbest}
        mycol.insert_one(data)

        dictred = pickle.dumps(data)
        r.set(f"bestfive{loop2}", dictred)

        readdict = r.get(f'bestfive{loop2}')
        loop2 = loop2 + 1

        dict = pickle.loads(readdict)

    time.sleep(60)

    




