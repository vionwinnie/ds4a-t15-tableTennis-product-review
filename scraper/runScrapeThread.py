import scrapeThread
import connectMongo
import pandas as pd
import json 
import sys

def run_scraper(thread_file,start_idx,end_idx):
    ## Initialize connection to mongoDB
    conn = connectMongo.connect_mongo('forums','tableTennisDaily')
    thread_df = pd.read_csv(thread_file)
    print(thread_df.columns)

    base_path = 'https://www.tabletennisdaily.com/forum'

    for row in thread_df.iterrows():
        attributes = row[1]
        thread_title = attributes['thread_title']
        link = attributes['URL']
        author = attributes['author']
        num_reply = attributes['num_reply']
    
        if row[0]>=start_idx and row[0]<end_idx:
            scrape_url = "{base_url}/{thread_link}".format(base_url=base_path,thread_link=link)
            df = scrapeThread.scrape_thread(scrape_url,local=False)

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

if __name__=="__main__":
    thread_file = '../output/tabletennisdaily_rubber_threads.csv'
    start_idx = int(sys.argv[1])
    end_idx = int(sys.argv[2])
    run_scraper(thread_file,start_idx,end_idx)
