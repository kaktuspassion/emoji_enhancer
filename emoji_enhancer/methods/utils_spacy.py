import spacy
from typing import Tuple, List

# Load the spaCy model
nlp = spacy.load('en_core_web_lg')
lemmatizer = nlp.get_pipe("lemmatizer")

# Load the emoji2vec dictionary from txt file
emoji2vec_dict = {}
with open("data/emoji2vec_dictionary.txt", "r", encoding="utf-8") as file:
    for line in file:
        phrase, emoji = line.strip().split('\t')
        if emoji in emoji2vec_dict:
            emoji2vec_dict[emoji].append(phrase)
        else:
            emoji2vec_dict[emoji] = [phrase]


def find_closest_emojis(word: str) -> List[Tuple[str, float]]:
    try:
        word_doc = nlp(word)
        if not word_doc.has_vector:
            return []
        
        similarities = []

        for emoji, phrases in emoji2vec_dict.items():
            max_similarity = 0
            for phrase in phrases:
                phrase_doc = nlp(phrase)
                if phrase_doc.has_vector:
                    similarity = word_doc.similarity(phrase_doc)
                    if similarity > max_similarity:
                        max_similarity = similarity
            similarities.append((emoji, max_similarity))
        
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
