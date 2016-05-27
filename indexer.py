from Engine.FuzzySearch import Trie
from Engine.LanguageModel import LanguageModel
from Engine.utils.utils import save_obj, load_obj

if __name__ == "__main__":
    PATH = "queries_all.txt"

    trie = Trie(PATH)
    save_obj(trie, "objects/Trie")
    trie = None

    lm = LanguageModel(PATH)
    save_obj(lm, "objects/LanguageModel")
    lm = None