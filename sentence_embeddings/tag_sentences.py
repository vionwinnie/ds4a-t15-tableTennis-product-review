## Tag Sentences based on Rubber names

import pandas as pd
import re
import csv
import nltk

pd.options.mode.chained_assignment = None

# load the dictionary
def csv2dict(fn):
    with open(fn) as f:
        reader = csv.reader(f)
        d = list(reader)
    return {k:v for (k,v) in d}

def csv2list(fn):
    with open(fn) as f:
        reader = csv.reader(f)
        d = list(reader)
    return [r[0] for r in d]


def sub_rubber_names(s,regex):
    if isinstance(s, str):
        return regex.sub(lambda m: rub_dict[m.group(0).lower()],s)
    else:
        return ''

# tokenize words, and remove stop words (if b_rm)
# then do pos tagging
def word_process(s, b_rm=0):
    wo = nltk.word_tokenize(s)
#    sw_include_list = 'than, as'
#    if b_rm:
#        wo = [w for w in wo if w not in nltk.corpus.stopwords.words('english') or w in sw_include_list]
    wo_pt = nltk.pos_tag(wo)
    return wo_pt


def find_rubbers(s_words):
    l = []
    for (w, t) in s_words:
        if t == 'NNP' and w not in l:
            l.append(w)
        elif w in rub_list and w not in l:
            l.append(w)
    return l

def process_raw_data(file_name):
    df = pd.read_csv(file_name)
    df.loc[:,'reply_sub'] = df['reply_split'].apply(sub_rubber_names,regex=regex)

    df['reply_words'] = ''
    df.loc[:,'reply_words'] = df['reply_sub'].apply(word_process)
    df.loc[:,'entity'] = df['reply_words'].apply(find_rubbers)

    cond1 = df.classification=='descriptive'
    cond2 = df.entity.apply(len)==1
    short_df = df[cond1&cond2]

    return short_df

if __name__ == '__main__':
    home_dir = '/home/winnie/tableTennis-product-review'
    rub_dict = csv2dict(home_dir+'/information_retrieval/rubber_dictionary/rub_dict.csv')
    rub_list = csv2list(home_dir+'/information_retrieval/rubber_dictionary/rub_name_list.csv')

    regex = re.compile(r'(?<!\w)(' + '|'.join(re.escape(key) for key in rub_dict.keys()) + r')(?!\w)',re.IGNORECASE)

    file_dir = home_dir + '/comparison/results/'
    filenames = ['final_eval_1.csv','final_eval_2.csv','final_eval_3.csv']

    processed_dfs = []

    for file in filenames:
        full_file_path = file_dir + file
        processed_df = process_raw_data(full_file_path)
        print(processed_df.shape)
        processed_dfs.append(processed_df)

    all_processed_df = pd.concat(processed_dfs,axis=0)
