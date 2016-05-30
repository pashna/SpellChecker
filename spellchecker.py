import sys
from Engine.utils.utils import load_obj, print_error
from Engine.ErrorModel import ErrorModel
from Engine.CorrectionSelector import CorrectionSelector
from Engine.TextFormatter import TextFormatter
from Engine.Classifier.QueryClassifier import QueryClassifier
from Engine.Generators.LayoutGenerator import LayoutGenerator
from Engine.Generators.SplitGenerator import SplitGenerator
from Engine.Generators.JoinGenerator import JoinGenerator
from time import time
from copy import copy

if __name__ == "__main__":

    lm = load_obj("LanguageModel")
    em = ErrorModel(load_obj("Trie"))
    cl = load_obj("classifier")
    qc = QueryClassifier(cl, lm)

    layoutGenerator = LayoutGenerator()
    splitGenerator = SplitGenerator()
    joinGenerator = JoinGenerator()
    cs = CorrectionSelector(em, lm)

    i = 0
    for s in sys.stdin:
        i+=1
        textFormatter = TextFormatter(s)
        words = textFormatter.get_query_list()
        query = textFormatter.text

        if qc.is_correct(query, words):
            print query.encode("utf-8")
            #print_error("{} \t OK".format(s))
        else:
            correction = []
            probs = []


            # =============================== Layout
            keybordChangedWords = layoutGenerator.generate_correction(words)
            queryKeybord = textFormatter.format_text(keybordChangedWords)
            if qc.is_correct(queryKeybord, keybordChangedWords):
                correction.append(queryKeybord.encode("utf-8"))
                probs.append(lm.get_prob(keybordChangedWords))


            # ================================= Grammar
            grammarWords = copy(words)
            for i in range(len(grammarWords)):
                word = grammarWords[i]
                if not lm.dict.has_key(word):
                    grammarWords = cs.fix(grammarWords, i)
                    queryGrammar = textFormatter.format_text(grammarWords)
                    if qc.is_correct(queryGrammar, grammarWords):
                        correction.append(queryGrammar.encode("utf-8"))
                        probs.append(lm.get_prob(grammarWords))


            # ================================ Join
            joins = joinGenerator.generate_joins(words)
            for join in joins:
                queryJoin = u" ".join(join)
                if qc.is_correct(queryJoin, join):
                    correction.append(queryJoin.encode("utf-8"))
                    probs.append(lm.get_prob(join))


            # ================================ Split
            splits = splitGenerator.generate_splits(words)
            for split in splits:
                querySplit = u" ".join(split)
                if qc.is_correct(querySplit, split):
                    correction.append(querySplit.encode("utf-8"))
                    probs.append(lm.get_prob(split))

            if len(correction) == 0:
                print query.encode("utf-8")
            else:
                print correction[probs.index(max(probs))]