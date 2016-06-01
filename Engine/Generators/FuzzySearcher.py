# coding: utf-8
#!/usr/bin/python
import re

class Trie:

    def __init__(self, words):
        self.trie = TrieNode()
        self.__regex = re.compile(r"[\w\d]+")
        self.__read(words)


    def __read(self, words):

        for word in words:
            self.trie.insert( word )


    def search(self, word, max_lev):

        currentRow = range( len(word) + 1 )
        results = []

        for letter in self.trie.children:
            self.searchRecursive(self.trie.children[letter], letter, word, currentRow, results, max_lev)

        return results


    def searchRecursive(self, node, letter, word, previousRow, results, max_lev):

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


        if currentRow[-1] <= max_lev and node.word != None:
            results.append( [node.word, currentRow[-1] ] )

        if min( currentRow ) <= max_lev:
            for letter in node.children:
                self.searchRecursive(node.children[letter], letter, word, currentRow, results, max_lev)


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