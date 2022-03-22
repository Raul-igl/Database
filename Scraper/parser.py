import redis
import pickle

r = redis.Redis(host='localhost', port=6379)

tel = 0
for i in range(0,50):
    read_dict = r.get(f'mydict{tel}')
    tel = tel + 1

    yourdict = pickle.loads(read_dict)

    print(yourdict)