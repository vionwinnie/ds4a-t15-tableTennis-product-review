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
    threads = soup.find('div', id='threadlist')
    ## Collects li of all threads
    posts = threads.findAll('li',{"class": "threadbit new"})
    posts.extend(threads.findAll('li',{"class": "threadbit hot"}))
    posts.extend(threads.findAll('li',{"class": "threadbit hot attachments"}))
    print(len(posts))
    
    if len(posts)==0:
        raise ValueError("this page has no posts")
    
    ## Collect thread information
    all_threads = []
    all_links = []
    all_author = []
    all_reply = []

    for post in posts:
        thread = post.find('a',{"class":"title"})
        all_threads.append(thread.text)
        all_links.append((thread['href']))
    
        author = post.find('a',{"class":"username understate"})
        all_author.append(author.text)

        stats = post.find('ul',{"class":"threadstats td alt"})
        num_reply = stats.find('a',{"class":"understate"}).text
        all_reply.append(num_reply)


    df = pd.DataFrame({"thread_title":all_threads,
                           "URL":all_links,
                           "author":all_author,
                           "num_reply":all_reply})

    return df 

if __name__ == "__main__":
    df = scrape_links('../rawData/test-Rubbers.html',local=True)    
    df.to_csv("../output/tmp.csv",index=False)
    print(df.shape)
    for title in df.thread_title:
        print(title)
    test_url = "https://www.tabletennisdaily.com/forum/forumdisplay.php?102-Rubbers/page1"

    df2 = scrape_links(test_url,local=False)
    df2.to_csv("../output/tmp2.csv",index=False)
    print(df2.shape)
    for title in df2.thread_title:
        print(title)
