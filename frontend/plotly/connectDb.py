import pandas as pd
import sqlite3

def connect_to_db(local=True):
    """ 
    initialize connection to local sqlite3
    """
    con = None
    if local:
        # Create a SQL connection to our SQLite database
        con = sqlite3.connect("./db/tableTennisData.db")
    
    return con 

def retrieve_data(query):
    con = connect_to_db()
    df = pd.read_sql_query(query, con)
    con.close()
    return df

def retrieve_two_rubbers_stats(entity1,entity2,transpose=True):
    query = """select * from rubbers where name in ('{}','{}')""".format(entity1,entity2)
    df = retrieve_data(query)
    if transpose:
        df = df.transpose()
    df.reset_index(inplace=True)
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    return df

if __name__=="__main__":
    #con = connect_to_db()

    entity1 ='DHS Hurricane 3 (H3)' 
    entity2 = 'Butterfly Tenergy 05'

    df = retrieve_two_rubbers_stats(entity1,entity2,transpose=True)
    if len(df) > 0:
        for row in df.iterrows():
            print(row[1])
    #df2 = df.transpose()
    #print(df2.head())
    # Be sure to close the connection
    #con.close()
