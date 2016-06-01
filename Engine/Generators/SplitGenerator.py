# coding: utf-8
from copy import copy
class SplitGenerator:

    def __init__(self, lm):
        self.lm = lm

    def generate_splits(self, words):
        splits = []

        for i in range(len(words)):
            word = words[i]

            if self.lm.dict.has_key(word):
                continue

            for j in range(1, len(word)):
                split = words[0:i]
                split.append(word[0:j])
                split.append(word[j:])
                split.extend(words[i+1:])

                splits.append(split)

        return splits