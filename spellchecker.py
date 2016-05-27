# coding: utf-8
import sys
from Engine.utils.utils import load_obj
from Engine.ErrorModel import ErrorModel
from Engine.CorrectionSelector import CorrectionSelector

if __name__ == "__main__":

    lm = load_obj("LanguageModel")
    em = ErrorModel(load_obj("Trie"))

    cs = CorrectionSelector(em, lm)

    """
    query = ["хоккей", "чемпионат", "мира", "смотрет"]

    for w in cs.fix(query, 3):
        print w
    """
    for s in sys.stdin:
        query=s.decode("utf-8")
        query = query[:-1]
        query = query.split(" ")
        for i in range(len(query)):
            word = query[i]

            if not lm.dict.has_key(word):
                query = cs.fix(query, i)

        for i in range(len(query)):
            query[i] = query[i].encode("utf-8")

        print " ".join(query)