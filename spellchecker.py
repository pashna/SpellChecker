# coding: utf-8
import sys
from Engine.utils.utils import load_obj
from Engine.ErrorModel import ErrorModel
from Engine.CorrectionSelector import CorrectionSelector
from Engine.TextFormatter import TextFormatter

if __name__ == "__main__":

    lm = load_obj("LanguageModel")
    em = ErrorModel(load_obj("Trie"))
    #cl = load_obj("classifier")

    cs = CorrectionSelector(em, lm)

    for s in sys.stdin:
        textFormatter = TextFormatter(s)
        query = textFormatter.get_query_list()
        for i in range(len(query)):
            word = query[i]

            if not lm.dict.has_key(word):
                query = cs.fix(query, i)

        print textFormatter.format_text(query)