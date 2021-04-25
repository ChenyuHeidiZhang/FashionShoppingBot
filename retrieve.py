# An interactive script that retrieves an item based on the input.

from model import Retriever


if __name__ == "__main__":
    while True:
        input = # sentence or image
        mode = 'img'
        src_file = 'items.csv'
        retriever = Retriever(mode, src_file)
        top_items = retriever.retrieve(input)
        print(top_items)
