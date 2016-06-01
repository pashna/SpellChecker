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


def correctLayout(layoutGenerator, words, correction, probs):
    keybordChangedWords = layoutGenerator.generate_correction(words)
    all_generation.append(keybordChangedWords)
    queryKeybord = textFormatter.format_text(keybordChangedWords)
    if qc.is_correct(queryKeybord, keybordChangedWords):
        correction.append(queryKeybord)
        probs.append(lm.get_prob(keybordChangedWords))


def correctGrammar(grammarGenerator, words, correction, probs):
    grammas = grammarGenerator.generate_correction(words)
    for gramma in grammas:
        all_generation.append(gramma)
        queryGramma = textFormatter.format_text(gramma)
        if qc.is_correct(queryGramma, gramma):
            correction.append(queryGramma)
            probs.append(lm.get_prob(gramma))


def correctJoin(joinGenerator, words, correction, probs):
    joins = joinGenerator.generate_joins(words)
    all_generation.extend(joins)
    for join in joins:
        queryJoin = u" ".join(join)
        if qc.is_correct(queryJoin, join):
            correction.append(queryJoin)
            probs.append(lm.get_prob(join))


def correctSplit(splitGenerator, words, correction, probs):
    splits = splitGenerator.generate_splits(words)
    all_generation.extend(splits)
    for split in splits:
        querySplit = u" ".join(split)
        if qc.is_correct(querySplit, split):
            correction.append(querySplit)
            probs.append(lm.get_prob(split))


def correct(layoutGenerator, grammarGenerator, joinGenerator, splitGenerator, words, correction, probs):
    correctLayout(layoutGenerator, words, correction, probs)
    correctGrammar(grammarGenerator, words, correction, probs)
    correctJoin(joinGenerator, words, correction, probs)
    correctSplit(splitGenerator, words, correction, probs)


if __name__ == "__main__":

    MAX_ITER = 2

    lm = load_obj("LanguageModel")
    em = load_obj("ErrorModel")
    #qc_input = QueryClassifier(load_obj("classifier_input"), lm)
    qc = QueryClassifier(load_obj("classifier"), lm)

    layoutGenerator = LayoutGenerator()
    splitGenerator = SplitGenerator(lm)
    joinGenerator = JoinGenerator()
    grammarGenerator = GrammarGenerator(em, lm)

    for s in sys.stdin:
        t = time()
        textFormatter = TextFormatter(s)
        words = textFormatter.get_query_list()
        query = textFormatter.text
        if qc.is_correct(query, words):
            print query.encode("utf-8")

        else:
            iteration = MAX_ITER
            found = False
            while iteration > 0 and not found:
                iteration -= 1

                correction = []
                all_generation = []
                probs = []

                correct(layoutGenerator, grammarGenerator, joinGenerator, splitGenerator, words, correction, probs)

                if len(correction) != 0:
                    print correction[probs.index(max(probs))].encode("utf-8")
                    found = True
                else:
                    gen_prob = []
                    for g in all_generation:
                        gen_prob.append(lm.get_prob(g))
                    words = all_generation[gen_prob.index(max(gen_prob))]
                    words = list(words)

            if not found:
                print textFormatter.format_text(words).encode("utf-8")

            #print "{} for {} iter".format(t-time(), MAX_ITER-iteration)