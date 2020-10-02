import connectMongo

## Example of how to fetch data from MongoDB

## current forum options are 'tableTennisDaily' and 'ooakForum'
forum_name = 'ooakForum'
conn = connectMongo.connect_mongo('forums',forum_name)
myquery = { "meta_idx": { "$gt": 870 } }
mydoc = conn.find(myquery)

for i,this_doc in enumerate(mydoc):
    if i <5:
        ## this_doc is a dictionary

        ## Iterate through key-value pair of the outer dictionary
        #for key,val in this_doc.items():
        #    print("{} with this value {}".format(key,val))

        ## extract the replies field (which is an array)
        replies = this_doc['replies']
        for reply in replies:
            print("===================================")
            ## each reply is in dictionary form
            print(reply['clean_text'])

