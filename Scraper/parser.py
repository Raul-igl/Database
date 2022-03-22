import redis
import pickle
import pymongo

r = redis.Redis(host='localhost', port=6379)
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")

tel = 0
for i in range(0,50):
    read_dict = r.get(f'mydict{tel}')
    tel = tel + 1

    onerow = pickle.loads(read_dict)

    databaseredis = client["databaseredis"]
    rij = databaseredis["Bestfive"]
    #rij.insert_many(onerow)

