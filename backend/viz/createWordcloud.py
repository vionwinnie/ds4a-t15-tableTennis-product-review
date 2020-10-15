from common import cleanData
from wordcloud import WordCloud
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def similar_color_func_red(word=None, font_size=None,
                       position=None, orientation=None,
                       font_path=None, random_state=None):
    h = 0 # 0 - 360
    s = 100 # 0 - 100
    l = random_state.randint(30, 80) # 0 - 100
    return "hsl({}, {}%, {}%)".format(h, s, l)

def similar_color_func_black(word=None, font_size=None,
                       position=None, orientation=None,
                       font_path=None, random_state=None):
    h = 0 # 0 - 360
    s = 0 # 0 - 100
    l = random_state.randint(30, 80) # 0 - 100
    return "hsl({}, {}%, {}%)".format(h, s, l)

def produce_wordcloud_graphics(word_list,stopwords,export_path,color):
    """
    input:
    word_list: list of list of words
    stopwords: list of string
    
    export matplotlib to designated path
    """
    mask = np.array(Image.open('/home/winnie/petProjects/tableTennisRubber/ds4a-t15-tableTennis-product-review/backend/viz/Img/ping_pong_paddle.jpg'))
    n_max_words = 300
    img_mask = mask

    word_color_scheme = similar_color_func_red if color=='red' else similar_color_func_black
    wordcloud = WordCloud(
            #width=800,
            #height=600,
            background_color='white',
            stopwords=stopwords, #custom_stop,
            max_words=n_max_words,
            max_font_size=100,
            scale=3,
            random_state=1,
            mask=img_mask,
            width=mask.shape[1]*2,
            height=mask.shape[0]*2,
            color_func=word_color_scheme)
   
    wordcloud_red=wordcloud.generate(str(word_list))
    fig = plt.figure(1, figsize=(50, 50))
    plt.axis('off')
    plt.imshow(wordcloud_red)

    plt.savefig(export_path, bbox_inches='tight')
    #plt.savefig(export_path)
    plt.close(fig)

if __name__=="__main__":
    print("running script")


    



