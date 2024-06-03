import pytest
from emoji_enhancer.utils import find_closest_emojis, add_emoji_to_tokens

def test_find_closest_emojis():
    """Tests if function returns the list of emojis correctly."""
    result = find_closest_emojis('apple')
    assert isinstance(result, list) # Checks if the return type is a list
    assert len(result) > 0  # Checks that the returned list contains at least one emoji
    # Checks if each element returned is a tuple with two elements
    assert all(isinstance(pair, tuple) and len(pair) == 2 for pair in result)

def test_add_emoji_to_tokens():
    """Test if the function returns a list with text and a list of token and emojis."""
    text = "She likes apples."
    token_types = ['NOUN']
    _, tokens = add_emoji_to_tokens(text, token_types)
    assert isinstance(tokens, list) # Check if the return type is a list
    # Checks that the returned list of tokens correctly contains emoji
    assert any(token == 'apples' for token, emojis in tokens if emojis)
