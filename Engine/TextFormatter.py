# coding: utf-8


import re

class TextFormatter:

    def __init__(self, text):
        self.text = text

    def get_query_list(self):
        """
        Возвращает список слов из запроса
        :return:
        """
        self.text = self.text.decode("utf-8")
        self.text = self.text[:-1]
        self.init_words = re.findall(ur"(?u)\w+", self.text)
        self.separators = re.split(ur"(?u)\w+", self.text)[1:]

        self.text = self.text.lower()
        query = re.findall(ur"(?u)\w+", self.text)

        return query


    def format_text(self, query):
        "форматирует текст в соответствии с входными данными"

        formatted_query = ""
        for i in range(len(query)):
            word = query[i]
            if self.init_words[i][0].isupper():
                w = word[0].upper()
                word = word[1:]
                word = w + word
                #word = word.encode("utf-8")

            formatted_query += word
            formatted_query += self.separators[i].encode("utf-8")

        return formatted_query