from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
from random import randint
import check_yaml

def connect_mongo(database_name,collection_name):
    
    login_dict = check_yaml.get_login_info()
    ## info
    mongoDbUser=login_dict['user']
    db_name = database_name
    mongoDbPwd=login_dict['password'] #kvbHGmyEErXa984v'
    mongo_url = "mongodb+srv://{user_name}:{pwd}@cluster0.gwrcx.gcp.mongodb.net/{dbname}?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE".format(user_name=mongoDbUser,pwd=mongoDbPwd,dbname=db_name)
    client = MongoClient(mongo_url)
    db=getattr(client,database_name)
    mongo_collections = getattr(db,collection_name)
    
    return mongo_collections

if __name__=="__main__":
    conn = connect_mongo('forums','tableTennisDailyTracker')
    thread = {'date':'2020-04-15',
              'url': 'testing.com',
              'num_replies':5,
              'replies':['a','b','c']}
    result=conn.insert_one(thread)
    print(result)
