import redis
import pickle
import pymongo

r = redis.Redis(host='localhost', port=6379)
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
databaseredis = client["databaseredis"]
rij = databaseredis["Bestfive"]


tel = 0
tel2 = 0
for i in range(0,50):
    read_dict = r.get(f'fulldata{tel}')
    tel = tel + 1

    onerow = pickle.loads(read_dict)
    readdict = r.get(f'bestfive{tel2}')
    tel2 = tel2 + 1
    if tel2 == 5:
        break

    onerow = pickle.loads(read_dict)
    rij.insert_one(onerow)
    print(onerow['hash'])
