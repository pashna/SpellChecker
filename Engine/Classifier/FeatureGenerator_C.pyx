# coding: utf-8
import re
from langdetect import detect

class FeatureGenerator:

    def __init__(self, lm):
        self.lm = lm
        self.__en_regex = re.compile(r'[a-z]\$')

    def generate_features(self, query, words):
        """
        :param query: str
        :param words: list
        :return:
        """
        cdef float x[8]# = []
        #words = re.findall(ur"(?u)\w+", query)
        x[0] = len(words)# количество слов
        x[1] = len(query)# количество символов
        x[2] = self.lm.get_prob(words) # вероятность такого запроса
        cdef float max_prob = -1.
        cdef float min_prob = 2.

        cdef int count_of_words_in_dict = 0
        for word in words:
            prob = self.lm.get_word_prob(word)
            if prob > max_prob:
                max_prob = prob
            if prob < min_prob:
                min_prob = prob

            if self.lm.dict.has_key(word):
                count_of_words_in_dict += 1

        x[3] = max_prob # максимальная вероятность слова
        x[4] = min_prob # минимальная вероятность слова
        x[5] = len(words)-count_of_words_in_dict # сколько слов нет в словаре

        if u"," in query or \
            u"." in query or \
            u"'" in query or \
            u";" in query or \
            u"]" in query or \
            u"[" in query or \
            u"~" in query:
            x[6] = 1 # есть ли "плохие" символы в запросе
        else:
            x[6] = 0

        if self.__en_regex.find(query):
            lang = 1
        else:
            lang = 0

        x[7] = lang # язык


        return x