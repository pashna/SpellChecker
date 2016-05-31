# coding: utf-8
from copy import copy

class GrammarGenerator:

    def __init__(self, em, lm):
        """
        :param em: ErrorModel Object
        :param lm: LanguageModel Object
        """
        self.em = em
        self.lm = lm


    def generate_correction(self, words):
        correction = []
        grammarWords = copy(words)
        for i in range(len(grammarWords)):
            word = grammarWords[i]
            if self.lm.dict.has_key(word):
                max_lev = 1
            else:
                max_lev = 2

            word_correction = self.em.get_correction(word, max_lev)

            # TODO: нужно будет оптимизировать, пока пусть все будут - посмотрим качество
            for w, lev in word_correction:
                c = copy(words)
                c[i] = w
                correction.append(copy(c))
                """
                grammarWords = cs.fix(grammarWords, i)
                queryGrammar = textFormatter.format_text(grammarWords)
                if qc.is_correct(queryGrammar, grammarWords):
                    correction.append(queryGrammar.encode("utf-8"))
                    probs.append(lm.get_prob(grammarWords))
                """
        return correction


    def fix(self, query, word_idx):
        correction_words = self.em.get_correction(query[word_idx])
        if len(correction_words) == 0:
            return query


        """
        correction_probs = []

        for word, prob in correction_words:
            query[word_idx] = word
            correction_probs.append(self.lm.get_prob(query)*prob)

        #best_correction = correction_probs.index(max(correction_probs))
        #query[word_idx] = correction_words[best_correction][0]
        return query
        """