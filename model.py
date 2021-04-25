import encoder

class Retriever():
    def __init__(self, mode, src_file):
        self.mode = mode  # 'img' or 'text'
        self.src_file = src_file
        pass

    def similarity_func():
        pass

    def search(vectors, emb):
        pass

    def retrieve(input):
        ''' Retrieve items and return their urls using a vector model.
        '''
        if self.mode == 'img':
            emb = encoder.encode_img(input)
        else: 
            emb = encoder.encode_text(input)

        column = self.mode + '_repr'
        vectors = #
        top_items = self.search(vectors, emb)
        return top_items


