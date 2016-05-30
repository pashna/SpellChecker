import sys
from Engine.utils.utils import load_obj
from Engine.ErrorModel import ErrorModel
from Engine.CorrectionSelector import CorrectionSelector
from Engine.TextFormatter import TextFormatter
from Engine.Classifier.QueryClassifier import QueryClassifier
from Engine.Generators.LayoutGenerator import LayoutGenerator
from Engine.Generators.SplitGenerator import SplitGenerator
from Engine.Generators.JoinGenerator import JoinGenerator

if __name__ == "__main__":

    lm = load_obj("LanguageModel")
    em = ErrorModel(load_obj("Trie"))
    cl = load_obj("classifier")
    qc = QueryClassifier(cl, lm)

    layoutGenerator = LayoutGenerator()
    splitGenerator = SplitGenerator()
    joinGenerator = JoinGenerator()

    cs = CorrectionSelector(em, lm)

    for s in sys.stdin:
        textFormatter = TextFormatter(s)

        words = textFormatter.get_query_list()
        query = textFormatter.text

        if qc.is_correct(query, words):
            print query.encode("utf-8")

        else:
            isFixed = False
            # =============================== Layout
            if not isFixed:
                keybordChangedWords = layoutGenerator.generate_correction(words)
                queryKeybord = textFormatter.format_text(keybordChangedWords)
                if qc.is_correct(queryKeybord, keybordChangedWords):
                    print queryKeybord.encode("utf-8")
                    isFixed = True

            # ================================ Join
            if not isFixed:
                joins = joinGenerator.generate_joins(words)
                for join in joins:
                    queryJoin = u" ".join(join)
                    if qc.is_correct(queryJoin, join):
                        print queryJoin.encode("utf-8")
                        isFixed = True
                        break


            # ================================ Split
            if not isFixed:
                splits = splitGenerator.generate_splits(words)
                for split in splits:
                    querySplit = u" ".join(split)
                    if qc.is_correct(querySplit, split):
                        print querySplit.encode("utf-8")
                        isFixed = True
                        break

            # ================================= Grammar
            if not isFixed:
                for i in range(len(words)):
                    word = words[i]
                    if not lm.dict.has_key(word):
                        words = cs.fix(words, i)

                text = textFormatter.format_text(words)
                print text.encode("utf-8")
                isFixed = True