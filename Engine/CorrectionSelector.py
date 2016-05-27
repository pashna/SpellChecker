class CorrectionSelector:

    def __init__(self, em, lm):
        """
        :param em: ErrorModel Object
        :param lm: LanguageModel Object
        """
        self.em = em
        self.lm = lm


    def fix(self, query, word_idx):
        correction_words = self.em.get_correction(query[word_idx])
        if len(correction_words)==0:
            return query
        correction_probs = []

        for word, prob in correction_words:
            query[word_idx] = word
            correction_probs.append(self.lm.get_prob(query)*prob)

        best_correction = correction_probs.index(max(correction_probs))
        query[word_idx] = correction_words[best_correction][0]
        return query