# Group sentences by sentence embeddings
from sentence_transformers import SentenceTransformer
import pandas as pd

# Load pretrained model
model = SentenceTransformer('paraphrase-distilroberta-base-v1',device='cuda')
print("model is loaded")

# Load Sentences
descriptive_df = pd.read_csv('all_eval_with_entity.csv')
sentences = descriptive_df.reply_split
print("sentences are loaded ")

# Transform sentence into sentence_embeddings
sentence_embeddings = model.encode(sentences,device='cuda',batch_size=32)
print(sentence_embeddings.shape)

from sklearn.manifold import TSNE
two_dim_vector = TSNE(n_components = 2, random_state=0, perplexity = perplexity, learning_rate = learning_rate, n_iter = iteration).fit_transform(word_vectors)[:,:3]
