import pandas as pd
import numpy as np
from gensim.models import KeyedVectors

# Load word2vec model
w2v = KeyedVectors.load_word2vec_format("../models/GoogleNews-vectors-negative300.bin", binary=True)

# Load emojional dictionary
emoji_df = pd.read_csv("emojional_dictionary.csv")

# Creat a list to save output emoji embeddings
emoji_embeddings = []

# Calculate emoji embeddings
for index, row in emoji_df.iterrows():
    emoji = row[0]
    words = row[1:].dropna()
    
    # Split phrases into tokens
    tokens = []
    for phrase in words:
        tokens.extend(phrase.split())

    # Access word2vec embeddings
    valid_embeddings = [w2v[word] for word in tokens if word in w2v]
    
    if valid_embeddings:
        # Calculate average embedding as emoji embedding
        mean_embedding = np.mean(valid_embeddings, axis=0)
        emoji_embeddings.append({'emoji': emoji, 'embedding': mean_embedding.tolist()})
    else:
        print(f"No valid words found for emoji: {emoji}")

# Save emoji embeddings into file
emoji_embeddings = pd.DataFrame(emoji_embeddings)
emoji_embeddings.to_csv("emoji_embeddings.csv", index=False)
