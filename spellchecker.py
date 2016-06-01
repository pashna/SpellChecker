import sys
from copy import copy
from time import time

from Engine.Classifier.QueryClassifier import QueryClassifier
from Engine.ErrorModel import ErrorModel
from Engine.Generators.GrammarGenerator import GrammarGenerator
from Engine.Generators.JoinGenerator import JoinGenerator
from Engine.Generators.LayoutGenerator import LayoutGenerator
from Engine.Generators.SplitGenerator import SplitGenerator
from Engine.TextFormatter import TextFormatter
from Engine.utils.utils import load_obj, print_error

if __name__ == "__main__":

    lm = load_obj("LanguageModel")
    em = ErrorModel(load_obj("Trie"))
    qc_input = QueryClassifier(load_obj("classifier_input"), lm)
    qc = QueryClassifier(load_obj("classifier"), lm)


    layoutGenerator = LayoutGenerator()
    splitGenerator = SplitGenerator(lm)
    joinGenerator = JoinGenerator()
    grammarGenerator = GrammarGenerator(em, lm)

    i = 0
    for s in sys.stdin:
        t1 = time()
        i+=1
        textFormatter = TextFormatter(s)
        words = textFormatter.get_query_list()
        query = textFormatter.text
        #print query.encode("utf-8")
        #print_error(s)

        if qc_input.is_correct(query, words):
            print "OK"
            print query.encode("utf-8")
        else:
            correction = []
            probs = []

            # =============================== Layout
            keybordChangedWords = layoutGenerator.generate_correction(words)
            queryKeybord = textFormatter.format_text(keybordChangedWords)
            if qc.is_correct(queryKeybord, keybordChangedWords):
                correction.append(queryKeybord)
                probs.append(lm.get_prob(keybordChangedWords))


            # ================================= Grammar
            t1 = time()
            grammas = grammarGenerator.generate_correction(words)
            print "{} generating gramma.".format(time()-t1)
            t1 = time()
            j = 0
            for gramma in grammas:
                queryGramma = textFormatter.format_text(gramma)
                j += 1
                if qc.is_correct(queryGramma, gramma):
                    correction.append(queryGramma)
                    probs.append(lm.get_prob(gramma))
            print "{} checking gramma. LEN = {}".format(time()-t1, j)
            print ""
            # ================================ Join
            t1 = time()
            joins = joinGenerator.generate_joins(words)
            print "{} generating joins.".format(time()-t1)
            t1 = time()
            for join in joins:
                queryJoin = u" ".join(join)
                if qc.is_correct(queryJoin, join):
                    correction.append(queryJoin)
                    probs.append(lm.get_prob(join))
            print "{} checking joins. LEN = {}".format(time()-t1, len(joins))

            # ================================ Split
            t1 = time()
            splits = splitGenerator.generate_splits(words)
            print "{} generating splits.".format(time()-t1)
            t1 = time()
            for split in splits:
                querySplit = u" ".join(split)
                if qc.is_correct(querySplit, split):
                    correction.append(querySplit)
                    probs.append(lm.get_prob(split))
            print "{} checking splits. LEN = {}".format(time()-t1, len(splits))

            if len(correction) == 0:
                print "not found"
                print query.encode("utf-8")
                #print_error("{} \t {}".format(query.encode("utf-8"), "not found=("))
            else:
                print correction[probs.index(max(probs))].encode("utf-8")
                #print_error("{} \t {}".format(query.encode("utf-8"), correction[probs.index(max(probs))]))

