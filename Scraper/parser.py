import redis
import pickle
import pymongo

#once again make connection to redis and mongodb
r = redis.Redis(host='localhost', port=6379)
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")

#database to put all the data into
databasefull = client["databasefull"]
rij = databasefull["Onehash"]

tel = 0
#send all the data from redis to mongodb
for i in range(0,50):
    read_dict = r.get(f'fulldata{tel}')
    tel = tel + 1

    onerow = pickle.loads(read_dict)
    rij.insert_one(onerow)


