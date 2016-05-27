# coding: utf-8

class LanguageModel:

    def __init__(self, FILE_PATH):
        self.dict = {}
        self.__count_of_word = 0.
        self.__read(FILE_PATH)
        # TODO: Потом пройтись и перейти к вероятностям, или с делением норм?


    def __read(self, file):

        with open(file) as f:
            content = f.readlines()

        for line in content:
            line = line.lower()
            line = line[:-1]
            index = line.find('\t')
            if index > 0:
                line = line[index+1:]

            for word in line.split(' '):
                if self.dict.has_key(word):
                    self.dict[word] += 1
                else:
                    self.dict[word] = 1

                self.__count_of_word += 1


    def __get_word_prob(self, word):
        if self.dict.has_key(word):
            return self.dict[word]/self.__count_of_word
        else:
            return 0.


    def get_prob(self, query):
        """
        :param query: list
        """
        prob = 1
        for w in query:
            prob *= self.__get_word_prob(w)

        return prob

"""
lm = LanguageModel("../data/small.txt")
print lm.get_prob(["секс", "анимированный"])
"""