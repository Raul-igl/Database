import redis
import pickle
import pymongo

r = redis.Redis(host='localhost', port=6379)
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
databaseredis = client["databaseredis"]
rij = databaseredis["Bestfive"]


tel = 0
for i in range(0,50):
    read_dict = r.get(f'mydict{tel}')
    tel = tel + 1

    onerow = pickle.loads(read_dict)
    rij.insert_one(onerow)
    print(onerow[0])
