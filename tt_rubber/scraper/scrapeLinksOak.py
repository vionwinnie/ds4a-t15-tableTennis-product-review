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
    threads = soup.find('div', id='pagecontent')
    ## Collects li of all threads
    posts = threads.findAll('tr')
    print(len(posts))
    if len(posts)==0:
        raise ValueError("this page has no posts")
    
    ## Collect thread information
    all_threads = []
    all_links = []
    all_author = []
    all_reply = []
    
    for post in posts:

        check = post.findAll('td',{"class":"row1"})
        if not check:
            print("this is an empty row, skipping")
            continue

        title = post.find('a',{"class": "topictitle"})
        title_text = title.text
        link = title['href']

        author = post.find('p',{"class":"topicauthor"}).text
        num_reply = post.find('p',{"class":"topicdetails"}).text

        all_threads.append(title_text)
        all_links.append(link)
        all_author.append(author)
        all_reply.append(num_reply)

        #print(title_text,link,author,num_reply)
    
    
    
    #for post in posts:
    #    all_threads.append(thread.text)
    #    all_links.append((thread['href']))
   # 
   #     author = post.find('a',{"class":"username understate"})
   #     all_author.append(author.text)

    #    stats = post.find('ul',{"class":"threadstats td alt"})
    #    num_reply = stats.find('a',{"class":"understate"}).text
    #    all_reply.append(num_reply)


    df = pd.DataFrame({"thread_title":all_threads,
                           "URL":all_links,
                           "author":all_author,
                           "num_reply":all_reply})

    return df 

if __name__ == "__main__":
    #df = scrape_links('../../rawData/ooak_raw.html',local=True)    
    #df.to_csv("../output/ooak_tmp.csv",index=False)
    #print(df.shape)
    #for title in df.thread_title:
    #    print(title)
    #test_url = "https://www.tabletennisdaily.com/forum/forumdisplay.php?102-Rubbers/page1"
    test_url = "https://ooakforum.com/viewforum.php?f=44&start=0"
    df2 = scrape_links(test_url,local=False)
    df2.to_csv("../output/tmp2.csv",index=False)
    print(df2.shape)
    for title in df2.thread_title:
       print(title)
