import os
import spacy
from typing import Tuple, List
from gensim.models import KeyedVectors
from gensim import downloader as api

# Print the Gensim cache directory path
print(f"Gensim cache directory: {api.BASE_DIR}")

# Load the spaCy model
nlp = spacy.load('en_core_web_lg')
lemmatizer = nlp.get_pipe("lemmatizer")

# Load the emojional emoji embeddings
e2v = KeyedVectors.load_word2vec_format("models/emojional.bin", binary=True)

# Load the pre-trained Google News word vectors 
w2v = api.load('word2vec-google-news-300')

def find_closest_emojis(word: str) -> List[Tuple[str, float]]:
    """
    Find and return the top five emojis(with similarity score) closest to a given word based on vector similarity.
    """
    try:
        word_vector = w2v.get_vector(word)
        top_emojis = e2v.most_similar(word_vector, topn=5)
        return [(emoji, similarity) for emoji, similarity in top_emojis]
    except (KeyError, IndexError):
        return []

    
def add_emoji_to_tokens(text: str, token_types: List[str]) -> Tuple[str, List[Tuple[str, List[Tuple[str, float]]]]]:
    """
    Analyze text and suggest emojis for tokens of specified types.
    """
    tokens_and_pos_tags = [(token.text, token.pos_) for token in nlp(text)]
    token_emoji_pairs = []

    for token, pos_tag in tokens_and_pos_tags:
        if pos_tag in token_types:
            top_emojis = find_closest_emojis(token)
            token_emoji_pairs.append((token, top_emojis))
        else:
            token_emoji_pairs.append((token, []))

    return text, token_emoji_pairs
