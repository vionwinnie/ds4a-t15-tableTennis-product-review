import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# from wordcloud import STOPWORDS
def get_stopwords():
    # stop = set(STOPWORDS)
    stop = stopwords.words('english')
    custom_words_sen = 'really, like, way, much , still, but, find, need, you, many, lot, always, say, could, well, even, the'

    custom_words = custom_words_sen.split(', ')

    custom_stop = stop + custom_words
    return custom_stop

def get_stopwords_list():
    stop_words =  ["i", "me", "my", "myself", "we", "our",
               "ours", "ourselves", "you", "your", "yours",
               "yourself", "yourselves", "he", "him", "his",
               "himself", "she", "her", "hers", "herself",
               "it", "its", "itself", "they", "them", "their",
               "theirs", "themselves", "what", "which", "who",
               "whom", "this", "that", "these", "those", "am",
               "is", "are", "was", "were", "be", "been", "being",
               "have", "has", "had", "having", "do", "does", "did",
               "doing", "a", "an", "the", "and", "but", "if", "or",
               "because", "as", "until", "while", "of", "at", "by",
               "for", "with", "about", "against", "between", "into",
               "through", "during", "before", "after", "above", "below",
               "to", "from", "up", "down", "in", "out", "on", "off",
               "over", "under", "again", "further", "then", "once",
               "here", "there", "when", "where", "why", "how", "all",
               "any", "both", "each", "few", "more", "most", "other",
               "some", "such", "no", "nor", "not", "only", "own", "same",
               "so", "than", "too", "very", "s", "t", "can", "will",
               "just", "don", "should", "now","would",'really',
               'like', 'way', 'much' , 'still', 'but', 'find', 'need',
               'many', 'lot', 'always', 'say', 'could', 'well', 'even', 'the','bit','much'
]
    return stop_words

def preprocess_news(df,col_name,lowercase=False):
    corpus=[]
    stem=PorterStemmer()
    lem=WordNetLemmatizer()
    stop = get_stopwords()
    for threads in df[col_name]:
        if lowercase == True:
            words=[str.lower(w) for w in word_tokenize(threads) if (w not in stop)]
        else:
            words=[w for w in word_tokenize(threads) if (w not in stop)]
        words=[lem.lemmatize(w) for w in words if len(w)>2]
        corpus.append(words)
    return corpus

def remove_dash(list_data):
    
    final_ = []
    for cur_sentence in list_data:
        for cur_word in cur_sentence:
            final_.append(cur_word.replace("'",''))
        
    return final_

