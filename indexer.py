import sys

from Engine.Generators.FuzzySearcher import Trie
from Engine.LanguageModel import LanguageModel
from Engine.utils.utils import save_obj

if __name__ == "__main__":
    sys.setrecursionlimit(50000)

    #PATH = "data/middle.txt"
    PATH = "queries_all.txt"

    lm = LanguageModel(PATH)
    save_obj(lm, "LanguageModel")


    trie = Trie(lm.dict.keys())
    save_obj(trie, "Trie")
    trie = None
