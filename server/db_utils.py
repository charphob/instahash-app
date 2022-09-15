import pymongo

""" Utility module for DB queries """
def db_conn():

    """ Connects to the MongoDB Atlas cloud DB and returns the db object """

    """
    DB is structured in such a way that each hashtag has it's own collection, which is equivalent to an SQL table.
    
    Each document in a hashtag collection is a single post scraped from RapidAPI Instagram API.
    
    Each document has the _id (primary key) chosen as the id field in the original request result.
    """
    from pymongo import MongoClient
    MONGO_URI = "mongodb+srv://charphob:w9KOgQmj041gYtDi@cluster0.6hktk.mongodb.net"

    client = MongoClient(MONGO_URI)

    db = client['instahash']

    

    return db


def find_ht(hashtag, t1=0, t2=0):

    """
    Returns a cursor to the query result set, which can then be iterated over.
    
    Method accepts hashtag only or with t1,t2 timestamps as date interval.

    The taken_at_timestamp is indexed with ascending sorting order inside the MongoDB indexing for faster access.

    If no date interval is provided, will query for entire collection, which is all posts of given hashtag.

    If date interval is provided, will query within range.
    """

    db = db_conn()
    ht_coll = db[hashtag]

    if t1 == 0 or t2 == 0:

        cursor = ht_coll.find(
            {}, {'_id': 0}
        )

    else:

        cursor = ht_coll.find(
            {'taken_at_timestamp': {'$gte': t1, '$lte': t2}}, {'_id': 0}
        )

    return cursor


def min_max_time():

    """
    Returns list of hashtags for search field autocomplete.

    Also returns 2 global minimum and maximum timestamp values across all documents in all collections to limit datepicker available dates (so that one won't be able to pick 1970/01/01).

    This should really be the minimum and maximum values for the specific searched hashtag, since unexpected results can occur.

    I have an idea of how to do it, haven't got to try to implement it.
    """

    db = db_conn()

    ht_min_list = []
    ht_max_list = []
    ht_list = []

    result = {}

    for coll_name in db.list_collection_names():

        ht_coll = db[coll_name]
        mx = ht_coll.find({}, {'taken_at_timestamp': 1, "_id": 0}).sort(
            'taken_at_timestamp', pymongo.DESCENDING).limit(1)[0].get('taken_at_timestamp')
        mn = ht_coll.find({}, {'taken_at_timestamp': 1, "_id": 0}).sort(
            'taken_at_timestamp', pymongo.ASCENDING).limit(1)[0].get('taken_at_timestamp')

        ht_min_list.append(mn)
        ht_max_list.append(mx)
        ht_list.append(ht_coll.name)

    global_min = min(ht_min_list)
    global_max = max(ht_max_list)

    result.update({"global_min": global_min, "global_max": global_max})
    result.update({'ht_list': ht_list})

    return result