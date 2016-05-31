# coding: utf-8
import re

class LanguageModel:

    def __init__(self, FILE_PATH):
        self.dict = {}
        self.__count_of_word = 0.
        self._regex = re.compile(r"\w+")
        self.__read(FILE_PATH)
        self.__normalize()


    def __read(self, file):

        with open(file) as f:
            content = f.readlines()

        for line in content:

            line=line.decode("utf-8")
            line = line.lower()
            line = line[:-1]
            index = line.find('\t')
            if index > 0:
                line = line[index+1:]

            words = re.findall(ur"(?u)\w+", line)
            for i in range(len(words)):
                word = words[i]

                if self.dict.has_key(word):
                    self.dict[word]["freq"] += 1.
                else:
                    self.dict[word] = {"freq": 1.,
                                       "words": {}}

                self.__count_of_word += 1


                # Заполняем статистику зависимости слов друг от друга
                if i!=len(words)-1:
                    if self.dict[word]["words"].has_key(words[i+1]):
                        self.dict[word]["words"][words[i+1]] += 1.
                    else:
                        self.dict[word]["words"][words[i+1]] = 1.


    def __normalize(self):
        """
        Нормализуем все данные
        :return:
        """
        for key, value in self.dict.iteritems():
            value["freq"] /= self.__count_of_word

            count_of_uses = sum(value["words"].values())

            for word, freq in value["words"].iteritems():
                value["words"][word] /= count_of_uses


    def __get_word_prob(self, w1, w2):
        """
            P(w1|w2)
            :param w1:
            :param w2:
        """
        try:
            w2_prob = 1e-8
            if self.dict[w1]["words"].has_key(w2):
                w2_prob = self.dict[w1]["words"][w2]
            return self.dict[w1]["freq"] * w2_prob

        except Exception:
            return 1e-12


    def get_prob(self, query):
        """
        :param query: list
        """
        if len(query) == 0:
            return 0.
        prob = 1
        for i in range(len(query)-1):
            w1 = query[i]
            w2 = query[i+1]
            prob *= self.__get_word_prob(w1, w2)

        if self.dict.has_key(query[-1]):
            prob *= self.dict[query[-1]]["freq"]

        return prob


    def get_word_prob(self, word):
        if self.dict.has_key(word):
            return self.dict[word]["freq"]
        else:
            return 0.