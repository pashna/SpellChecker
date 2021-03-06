import sys

from Engine.Generators.FuzzySearcher import Trie
from Engine.LanguageModel import LanguageModel
from Engine.utils.utils import save_obj
from Engine.ErrorModel import ErrorModel


if __name__ == "__main__":
    sys.setrecursionlimit(50000)

    PATH = "queries_all.txt"

    lm = LanguageModel(PATH)
    save_obj(lm, "LanguageModel")

    trie = Trie(lm.dict.keys())

    em = ErrorModel(trie, PATH)
    save_obj(em, "ErrorModel")