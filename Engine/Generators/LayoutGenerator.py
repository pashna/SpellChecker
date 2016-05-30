# coding: utf-8

class LayoutGenerator:
    keybord = {
u'й': u'q', u'ц': u'w', u'у': u'e', u'к': u'r', u'е': u't', u'н': u'y', u'г': u'u',
u'ш': u'i', u'щ': u'o', u'з': u'p', u'х': u'[', u'ъ': u']', u'ф': u'a', u'ы': u's',
u'в': u'd', u'а': u'f', u'п': u'g', u'р': u'h', u'о': u'j', u'л': u'k', u'д': u'l',
u'ж': u';', u'э': u"'", u'я': u'z', u'ч': u'x', u'с': u'c', u'м': u'v', u'и': u'b',
u'т': u'n', u'ь': u'm', u'б': u',', u'ю': u'.', u'q': u'й', u'w': u'ц', u'e': u'у',
u'r': u'к', u't': u'е', u'y': u'н', u'u': u'г', u'i': u'ш', u'o': u'щ', u'p': u'з',
u'[': u'х', u']': u'ъ', u'a': u'ф', u's': u'ы', u'd': u'в', u'f': u'а', u'g': u'п',
u'h': u'р', u'j': u'о', u'k': u'л', u'l': u'д', u';': u'ж', u"'": u'э', u'z': u'я',
u'x': u'ч', u'c': u'с', u'v': u'м', u'b': u'и', u'n': u'т', u'm': u'ь', u',': u'б', u'.': u'ю',
}

    def __init__(self):
        pass
    #TODO: +ОТДЕЛЬНЫЕ СЛОВА


    def change_layour(self, word):
        new_word = u""
        for w in word:
            try:
                new_word += LayoutGenerator.keybord[w]
            except Exception:
                new_word += w
        return new_word


    def generate_correction(self, words):
        """
        :param query: str
        """
        query = []
        for w in words:
            query.append(self.change_layour(w))
        return query


"""
a = u"йцукенгшщзхъфывапролджэячсмитьбю"
b = u"qwertyuiop[]asdfghjkl;'zxcvbnm,."

print u"{"
for i in range(len(b)):
    print u"u'{}': u'{}',".format(a[i], b[i])

for i in range(len(b)):
    print u"u'{}': u'{}',".format(b[i], a[i])

print u"}"
"""

#print LayoutGenerator().change_layour("ghbdtn")