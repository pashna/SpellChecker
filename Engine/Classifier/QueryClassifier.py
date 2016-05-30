from FeatureGenerator import FeatureGenerator

class QueryClassifier:

    def __init__(self, cl, lm):
        self.cl = cl
        self.fg = FeatureGenerator(lm)


    def is_correct(self, query, words):
        x = [self.fg.generate_features(query, words)]
        return self.cl.predict(x)[0]