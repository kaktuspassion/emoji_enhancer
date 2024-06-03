import argparse
from emoji_enhancer.utils import add_emoji_to_tokens


def parse_arguments():
    """
    Parse the command-line arguments.
    """
    parser = argparse.ArgumentParser(description='Enhance text with emojis.')
    parser.add_argument('text', type=str, help='The text to enhance with emojis.')
    parser.add_argument('-n', '--nouns', action='store_true', help='Add emojis to nouns')
    parser.add_argument('-v', '--verbs', action='store_true', help='Add emojis to verbs')
    parser.add_argument('-adj', '--adjectives', action='store_true', help='Add emojis to adjectives')
    parser.add_argument('-adv', '--adverbs', action='store_true', help='Add emojis to adverbs')
    return parser.parse_args()

def main():
    """
    Main function to enhance text according to user's options.
    """
    # Parse command-line arguments
    args = parse_arguments()

    # Determine the types of tokens to add emojis to
    token_types = ['NOUN', 'VERB', 'ADJ', 'ADV']
    if args.nouns:
        token_types = ['NOUN']
    if args.verbs:
        token_types = ['VERB']
    if args.adjectives:
        token_types = ['ADJ']
    if args.adverbs:
        token_types = ['ADV']
    
    # Enhance the text with emojis, get the revised text and replaced tokens
    revised_text, replaced_tokens = add_emoji_to_tokens(args.text, token_types)

    # Iterate through tokens and let user choose from all emoji options
    for token, emojis in replaced_tokens:
        if emojis:
            print(f"Options for {token}:")
            for i, (emoji, score) in enumerate(emojis, 1):
                print(f"{i}. {emoji} ({score:.2f})")
            print("6. Reject all")
            choice = input("Enter your choice (number): ")
            if choice != '6':
                index = int(choice) - 1
                revised_text = revised_text.replace(f"{token}", f"{token}{emojis[index][0]}")

    print("Revised text:", revised_text)
    
if __name__ == '__main__':
    main()