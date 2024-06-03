import spacy
from typing import Tuple, List
from gensim import downloader as api
import numpy as np 
import pandas as pd
import ast

print(f"Gensim cache directory: {api.BASE_DIR}")

# Load the spaCy model
nlp = spacy.load('en_core_web_lg')
lemmatizer = nlp.get_pipe("lemmatizer")

# Load the google word2vec embeddings model 
w2v = api.load('word2vec-google-news-300')

# Load the emoji embeddings from CSV
emoji_embeddings_df = pd.read_csv("model/emoji_embeddings.csv")

# Convert emoji embeddings to a dictionary for quick lookup
emoji_embeddings = {row['emoji']: np.array(ast.literal_eval(row['embedding']), dtype=float) for _, row in emoji_embeddings_df.iterrows()}


def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def find_closest_emojis(word: str) -> List[Tuple[str, float]]:
    try:
        word_vector = w2v.get_vector(word)
        similarities = []
        
        for emoji, embedding in emoji_embeddings.items():
            similarity = cosine_similarity(word_vector, embedding)
            similarities.append((emoji, similarity))
        
        # Sort by similarity and get top 5
        top_emojis = sorted(similarities, key=lambda x: x[1], reverse=True)[:5]
        return top_emojis
    except (KeyError, IndexError):
        return []

def add_emoji_to_tokens(text: str, token_types: List[str]) -> Tuple[str, List[Tuple[str, List[Tuple[str, float]]]]]:
    tokens_and_pos_tags = [(token.text, token.pos_) for token in nlp(text)]
    token_emoji_pairs = []

    for token, pos_tag in tokens_and_pos_tags:
        if pos_tag in token_types:
            top_emojis = find_closest_emojis(token)
            token_emoji_pairs.append((token, top_emojis))
        else:
            token_emoji_pairs.append((token, []))

    return text, token_emoji_pairs
