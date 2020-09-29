import scrapeThreadMyTt
import connectMongo
import pandas as pd
import json 
import sys
import re

def run_scraper(thread_file,start_idx,end_idx):
    ## Initialize connection to mongoDB
    conn = connectMongo.connect_mongo('forums','myTt')
    thread_df = pd.read_csv(thread_file)
    print(thread_df.columns)

    base_url = "http://mytabletennis.net/forum"
    count = 0
    for row in thread_df.iterrows():

        count +=1
        attributes = row[1]
        thread_title = attributes['thread_title']
        link = attributes['URL']
        author = attributes['author']
        num_reply = attributes['num_reply']
        
        if row[0]>=start_idx and row[0]<end_idx:
            scrape_url = "{base_path}/{topic_name}".format(base_path=base_url,topic_name=link)
            print(scrape_url)
            try:
                df = scrapeThreadMyTt.scrape_thread(scrape_url,local=False)

                if df.shape[0]>0:
                    records = json.loads(df.to_json(orient='records'))
                    thread = {'meta_idx':row[0],
                          'title':thread_title,
                          'url': link,
                          'author':author,
                          'num_replies':num_reply,
                          'replies':records,
                          'sub-forum':'general'}
                    result=conn.insert_one(thread)
                    print("dataframe size :{}, with {}".format(df.shape,result))
                else:
                    print("skipping idx: {}".format(row[0]))
            except ValueError:
                print("idx :{}".format("cannot retrieve html"))
if __name__=="__main__":
    thread_file = '../output/mytabletennis_equipment_threads.csv'
    start_idx = int(sys.argv[1])
    end_idx = int(sys.argv[2])
    run_scraper(thread_file,start_idx,end_idx)
