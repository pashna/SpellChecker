# coding: utf-8
import difflib
import re
from math import sqrt

class ErrorModel:

    def __init__(self, fuzzy_searcher, file=None):
        self.fuzzy_searcher = fuzzy_searcher
        self.alpha = 1.5
        self.error_dict = {u'replace':{},
                           u'insert':{},
                           u'delete': {}}
        self.__cor_count = 0

        self.__fit(file)
        self.fuzzy_searcher.set_em(self)

    def __fit(self, file):
        with open(file) as f:
            content = f.readlines()

        for line in content:

            line=line.decode("utf-8")
            line = line.lower()
            line = line[:-1]
            index = line.find('\t')
            if index > 0:
                q = line.split('\t')
                if len(re.findall(ur"(?u)\w+", q[0])) == len(re.findall(ur"(?u)\w+", q[1])):
                    self.fill_dict(q[1], q[0])


    def fill_dict(self, query1, query2):
        inserts = []
        deletes = []
        for i,s in enumerate(difflib.ndiff(query1, query2)):
            if s[0]==' ': continue
            elif s[0]=='-':
                deletes.append((s[-1], i))#)print(u'Delete "{}" from position {}'.format(s[-1],i))
            elif s[0]=='+':
                inserts.append((s[-1], i))
            self.__cor_count += 1

        delete_mask = [True]*len(deletes)
        insert_mask = [True]*len(inserts)
        for i in range(len(inserts)):
            for i in range(len(deletes)):
                c1 = deletes[i][0]
                p1 = deletes[i][1]
                #replace = False
                for j in range(len(inserts)):
                    c2 = inserts[j][0]
                    p2 = inserts[j][1]
                    if abs(p2-p1) == 1:
                        #REPLACE
                        delete_mask[i] = False
                        insert_mask[j] = False
                        if not self.error_dict[u"replace"].has_key(c1):
                            self.error_dict[u"replace"][c1] = {}

                        if self.error_dict[u"replace"][c1].has_key(c2):
                           self.error_dict[u"replace"][c1][c2] += 1
                        else:
                            self.error_dict[u"replace"][c1][c2] = 1

            for i in range(len(deletes)):
                if delete_mask[i]:
                    c = deletes[i][0]
                    if  self.error_dict[u"delete"].has_key(c):
                        self.error_dict[u"delete"][c] += 1
                    else:
                        self.error_dict[u"delete"][c] = 1

            for i in range(len(inserts)):
                if insert_mask[i]:
                    c = inserts[i][0]
                    if  self.error_dict[u"insert"].has_key(c):
                        self.error_dict[u"insert"][c] += 1
                    else:
                        self.error_dict[u"insert"][c] = 1


    def __weight_func(self, count):
        return (0.65)**sqrt(count)


    def get_weight(self, type, c1, c2=None):
        if type == u"delete":
            if self.error_dict[u"delete"].has_key(c1):
                count = self.error_dict[u"delete"][c1]
            else:
                count = 0
        elif type == u"insert":
            if self.error_dict[u"insert"].has_key(c1):
                count = self.error_dict[u"insert"][c1]
            else:
                count = 0

        elif type == u'replace':
            if self.error_dict[u"replace"].has_key(c1):
                if self.error_dict[u"replace"][c1].has_key(c2):
                    count = self.error_dict[u"replace"][c1][c2]
                else:
                    count = 0
            else:
                count = 0

        return self.__weight_func(count)


    def get_correction(self, word, max_lev):
        correction = self.fuzzy_searcher.search(word, max_lev)

        for i in range(len(correction)):
            correction[i][1] = self.alpha**(-correction[i][1])

        return correction
