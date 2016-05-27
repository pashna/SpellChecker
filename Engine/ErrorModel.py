class ErrorModel:

    def __init__(self, fuzzy_searcher, alpha=2):
        self.fuzzy_searcher = fuzzy_searcher
        self.alpha = 1.5

    def get_correction(self, word):
        correction = self.fuzzy_searcher.search(word, 2)
        for i in range(len(correction)):
            correction[i][1] = self.alpha**(-correction[i][1])

        return correction