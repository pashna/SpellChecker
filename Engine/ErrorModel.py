class ErrorModel:

    def __init__(self, fuzzy_searcher, alpha=2):
        self.fuzzy_searcher = fuzzy_searcher
        self.alpha = 1.5

    def get_correction(self, word, max_lev):
        correction = self.fuzzy_searcher.search(word, max_lev)
        """
        for i in range(len(correction)):
            correction[i][1] = -correction[i][1]#self.alpha**(-correction[i][1])
        """
        return correction