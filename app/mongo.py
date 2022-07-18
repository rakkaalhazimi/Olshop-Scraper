import pymongo


def connect_cluster(username, password):
    client = pymongo.MongoClient(
        f"mongodb+srv://{username}:{password}@cluster0.0mxgk.mongodb.net/?retryWrites=true&w=majority")
    return client