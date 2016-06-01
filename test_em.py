# coding: utf-8
from Engine.utils.utils import load_obj

em = load_obj("ErrorModel")
print em.get_weight(u"replace", u"a", u"о")
print em.get_weight(u"replace", u"ъ", u"а")
