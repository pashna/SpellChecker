# coding: utf-8
from copy import copy
import itertools

class GrammarGenerator:

    def __init__(self, em, lm):
        # TODO: прекращать генерацию, если уже набралось достаточно кандидатов с меньшим Левинштейном
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
        grammarWords = copy(words)
        for i in range(len(grammarWords)):
            word = grammarWords[i]
            decart_of_correction.append([])

            if self.lm.dict.has_key(word):
                decart_of_correction[i].append(word)
                continue
            word_correction = self.em.get_correction(word, max_lev=2)
            word_correction = sorted(word_correction, key=lambda tup: tup[1])

            for w, lev in word_correction[:3]:
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