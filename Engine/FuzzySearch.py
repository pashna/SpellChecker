# coding: utf-8
#!/usr/bin/python

import time

DICTIONARY = "/usr/share/dict/words";
TARGET = "погода"
MAX_COST = 1


class Trie:

    def __init__(self, FILE_PATH):
        self.trie = TrieNode()
        self.__read(FILE_PATH)


    def __read(self, FILE_PATH):
        with open(FILE_PATH) as f:
            content = f.readlines()

        for line in content:
            line = line.lower()
            line = line[:-1]
            index = line.find('\t')
            if index > 0:
                line = line[index+1:]

            for word in line.split(' '):
                self.trie.insert( word )


    def search(self, word, maxCost ):

        currentRow = range( len(word) + 1 )
        results = []

        for letter in self.trie.children:
            self.searchRecursive( self.trie.children[letter], letter, word, currentRow, results, maxCost )

        return results


    def searchRecursive(self, node, letter, word, previousRow, results, maxCost ):

        columns = len( word ) + 1
        currentRow = [ previousRow[0] + 1 ]

        for column in xrange( 1, columns ):
            insertCost = currentRow[column - 1] + 1
            deleteCost = previousRow[column] + 1

            if word[column - 1] != letter:
                replaceCost = previousRow[ column - 1 ] + 1
            else:
                replaceCost = previousRow[ column - 1 ]

            currentRow.append( min( insertCost, deleteCost, replaceCost ) )

        if currentRow[-1] <= maxCost and node.word != None:
            results.append( (node.word, currentRow[-1] ) )

        if min( currentRow ) <= maxCost:
            for letter in node.children:
                self.searchRecursive( node.children[letter], letter, word, currentRow, results, maxCost )


class TrieNode:
    def __init__(self):
        self.word = None
        self.children = {}


    def insert( self, word ):
        node = self
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()

            node = node.children[letter]

        node.word = word

"""
t = Trie("../data/queries_all.txt")
start = time.time()
results = t.search( TARGET, MAX_COST )
end = time.time()
"""