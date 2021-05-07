# An interactive script that retrieves an item based on the input.

from model import Retriever

import validators
import os

if __name__ == "__main__":
    src_file = 'items.csv'
    print("Construsting retriever...")
    retriever = Retriever(src_file)
    print("Done")

    while True:
        user_input = input('Please input search query (text, or url/path to image): ')
        if os.path.exists(user_input) or validators.url(user_input):
            mode = 'img'
        else:
            mode = 'text'
        top_items = retriever.retrieve(user_input, mode)
        #print(top_items)
        print()
