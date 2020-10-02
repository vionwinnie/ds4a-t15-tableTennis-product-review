import scrapeLinksOak
import pandas as pd

#base_path = 'https://www.tabletennisdaily.com/forum/forumdisplay.php?102-Rubbers'
#base_path='https://www.tabletennisdaily.com/forum/forumdisplay.php?164-Butterfly'
#base_path = 'https://www.tabletennisdaily.com/forum/forumdisplay.php?177-Tibhar'
base_path = 'https://ooakforum.com/viewforum.php?f=44&start='

for i in range(0,2562,50):
    #print(i)

    
    page_path = "{base_path}{num}".format(base_path=base_path,num=i)
    print(page_path)

    cur_links = scrapeLinksOak.scrape_links(page_path,local=False)
    print(cur_links.shape)

    if i ==0:
        all_links = cur_links
    else:
        all_links = pd.concat([all_links,cur_links],axis=0)

    print(all_links.shape)
    
all_links.drop_duplicates(inplace=True)
print(all_links.shape)
output_path = '../output/ooak_invertedrubber_threads.csv'
all_links.to_csv(output_path,index=False)
print('export is completed')
