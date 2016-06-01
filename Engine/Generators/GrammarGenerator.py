# coding: utf-8
from copy import copy
import itertools
from time import time

class GrammarGenerator:

    def __init__(self, em, lm):
        """
        :param em: ErrorModel Object
        :param lm: LanguageModel Object
        """
        self.em = em
        self.lm = lm


    def generate_correction(self, words):
        """
        Тут учитывается расстояние и генериться "граф" всех вариантов.
        :param words:
        :return:
        """
        decart_of_correction = []

        for i in range(len(words)):
            word = words[i]
            decart_of_correction.append([])

            if self.lm.dict.has_key(word):
                decart_of_correction[i].append(word)
                continue
            t = time()
            word_correction = self.em.get_correction(word, max_lev=0.3)

            for w, lev in word_correction:
                decart_of_correction[-1].append(w)

            if self.lm.dict.has_key(word) or len(decart_of_correction[i]) == 0:
                #если слово есть в словаре или не нашлось близких к нему добавим изначальное слово
                decart_of_correction[i].append(word)

        correction = itertools.product(*decart_of_correction)

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
