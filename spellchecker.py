import sys
from Engine.utils.utils import load_obj
from Engine.ErrorModel import ErrorModel
from Engine.CorrectionSelector import CorrectionSelector
from Engine.TextFormatter import TextFormatter
from Engine.Classifier.QueryClassifier import QueryClassifier

if __name__ == "__main__":

    lm = load_obj("LanguageModel")
    em = ErrorModel(load_obj("Trie"))
    cl = load_obj("classifier")
    qc = QueryClassifier(cl, lm)

    cs = CorrectionSelector(em, lm)

    for s in sys.stdin:
        textFormatter = TextFormatter(s)

        words = textFormatter.get_query_list()
        query = textFormatter.text

        if qc.is_correct(query, words):
            print textFormatter.text.encode("utf-8")
        else:
            for i in range(len(words)):
                word = words[i]

                if not lm.dict.has_key(word):
                    words = cs.fix(words, i)

            text = textFormatter.format_text(words)
            print text.encode("utf-8")