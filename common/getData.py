from common import connectMongo
import re
import pandas as pd
import nltk
import ast
import time

## Example of how to fetch data from MongoDB
def get_sample_data(conn,largest_idx):
    
    ## current forum options are 'tableTennisDaily' and 'ooakForum'
    #forum_name = 'ooakForum'
    conn = connectMongo.connect_mongo('forums',forum_name)
    myquery = { "meta_idx": { "$gt": largest_idx } }
    mydoc = conn.find(myquery)

    return mydoc

def generate_df_from_result(result):
    """
    input: mongodb query result
    output: dataframe
    """
    ids = []
    titles = []
    replies = []

    for idx,val in enumerate(result):
        # add to the lists
        ids.append(val['_id'])
        titles.append(val['title'])
        replies_arr = []

        for reply in val['replies'][1:]: # don't want the original post asking the question so use [1:]
            text = reply['clean_text'].replace('\n','') # want to get rid of the \n\n
            replies_arr.append(text)
        replies.append(replies_arr)
    df = pd.DataFrame({'id':ids,'thread_title':titles,'reply':replies})
    df = df.explode('reply') # explode() to go from item in arr to row
    return df

def get_and_or_data(conn):
    # find all thread title that contains OR or '/' symbol (ignore case)
    regex_or = re.compile("( or )|(\/)", re.IGNORECASE)
    regex_or_result = conn.find({"title":regex_or},{"title":1,"replies.clean_text":1})
    or_df = generate_df_from_result(regex_or_result)

    # find all thread title that contains AND or '&' symbol (ignore case)
    regex_and = re.compile("( and )|(\&)", re.IGNORECASE)
    regex_and_result = conn.find({"title":regex_and},{"title":1,"replies.clean_text":1})
    and_df = generate_df_from_result(regex_and_result)
    
    combined_df = pd.concat([or_df,and_df])
    return combined_df

def get_vs_data(conn):
    # find all thread title that contains VS (ignore case)
    vs = re.compile("vs", re.IGNORECASE)
    vs_result = conn.find({"title":vs},{"title":1,"replies.clean_text":1})
    vs_df = generate_df_from_result(vs_result)

    return vs_df


def tokenize_sent(s):
    if pd.isna(s):
        return None
    else:
        s_split = s.split('\n') # ensures that \n is taken as a splitter
        s_split = [t for t in s_split if t]
        tokenized = list(map(nltk.sent_tokenize, s_split)) # list of lists
        return [t for sub in tokenized for t in sub] # flatten out




if __name__ == "__main__":
    forum_name = 'ooakForum'
    conn = connectMongo.connect_mongo('forums',forum_name)
    docs = get_sample_data(conn,807)
