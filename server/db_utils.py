from turtle import update
from unittest import result
import pymongo


def db_conn():

    from pymongo import MongoClient
    MONGO_URI = "mongodb+srv://charphob:w9KOgQmj041gYtDi@cluster0.6hktk.mongodb.net"

    client = MongoClient(MONGO_URI)

    db = client['instahash']

    return db


def find_ht(hashtag, t1=0, t2=0):

    db = db_conn()
    ht_coll = db[hashtag]

    if t1 == 0 or t2 == 0:

        cursor = ht_coll.find(
            {}, {'_id':0}
        )

    else:

        cursor = ht_coll.find(
            {'taken_at_timestamp': {'$gte': t1, '$lte': t2}}, {'_id':0}
        )

    return cursor

def min_max_time():

    db = db_conn()

    ht_min_list = []
    ht_max_list = []
    ht_list = []

    result = {}

    for coll_name in db.list_collection_names():

        ht_coll = db[coll_name]
        mx = ht_coll.find({},{'taken_at_timestamp':1,"_id":0}).sort('taken_at_timestamp',pymongo.DESCENDING).limit(1)[0].get('taken_at_timestamp')
        mn = ht_coll.find({},{'taken_at_timestamp':1,"_id":0}).sort('taken_at_timestamp',pymongo.ASCENDING).limit(1)[0].get('taken_at_timestamp')

        ht_min_list.append(mn)
        ht_max_list.append(mx)
        ht_list.append(ht_coll.name)
    
    global_min = min(ht_min_list)
    global_max = max(ht_max_list)

    result.update({"global_min":global_min,"global_max":global_max})
    result.update({'ht_list':ht_list})

    return result

# for i in find_ht('afula', 1439318756, 1451493151):

#     print(i.get('shortcode'), i.get('taken_at_timestamp'))

# print(len(list(find_ht('kfarkama',1,1663007061))))

# print(len(list(find_ht('afula', 1439318756, 1662000061))))

# print(find_ht('kfarkama')[0])