from bs4 import BeautifulSoup
import pandas as pd
import requests 

def scrape_links(url,local=True):
    if local:
        print("reading local file!")
        with open(url) as fp:
            soup = BeautifulSoup(fp,features="html.parser")
    else:
        page = requests.get(url)
        if page.status_code==200:
            soup = BeautifulSoup(page.text,features="html.parser")
        else:
            raise ValueError("requests unable to fetch the page")

    ## Identify the div that contains thread
    threads = soup.select('tr.evenTableRow,tr.oddTableRow')

    if len(threads)==0:
        raise ValueError("this page has no posts")
    
    ## Collect thread information
    all_threads = []
    all_links = []
    all_author = []
    all_reply = []
    
    for thread in threads:
        div_tag = thread.find('div',{'style':'float:left'})
        a_tag = div_tag.find('a')
        cur_thread = a_tag.text
        cur_link = a_tag['href']

        cur_reply = thread.findAll('td',{'align':'center'})[0].text
        last_post_div = thread.find('td',{'class':'smText'})
        cur_author = last_post_div.find('a',{'class':'smLink'}).text


#        print(cur_thread,cur_link,cur_reply,cur_author)


        all_threads.append(cur_thread)
        all_links.append(cur_link)
        all_reply.append(cur_reply)
        all_author.append(cur_author)

    df = pd.DataFrame({"thread_title":all_threads,
                           "URL":all_links,
                           "author":all_author,
                           "num_reply":all_reply})

    return df 
    

if __name__ == "__main__":
    #df = scrape_links('../../rawData/test-MyTableTennisNet.html',local=True)    
    #df.to_csv("../output/tmp.csv",index=False)
    #print(df.shape)
    #for title in df.thread_title:
    #    print(title)
    #test_url = "https://www.tabletennisdaily.com/forum/forumdisplay.php?102-Rubbers/page1"
    test_url = "http://mytabletennis.net/forum/equipment_forum24_page5.html"
    df2 = scrape_links(test_url,local=False)
    df2.to_csv("../output/tmp2.csv",index=False)
    print(df2.shape)
    for title in df2.thread_title:
        print(title)
