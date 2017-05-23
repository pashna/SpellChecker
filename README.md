# Spell Checker

An advanced Spell Checker using the Russian Language based on the search log of one the most popular Russian search engine Mail.Ru. The system uses **Machine Learning** and **Nautral Language Processing** techniques.

The spell checker can successfully resolve 4 types of mistypes:
* Layout errors
* Grammar errors
* Incorrect split
* Incorrect join

The system consists of:
* Language model, **P(queue)** (n-gramm probability model of the requests) 
* Error model, **P(fix|orig)** - the probability that user sent orig-request but actually wanted to send fix-request. Uses weighted **Levenshtein distance**.
* Fixes generator based on fuzzy string search to improve efficiency
* **Machine Learning** mistype classifier
* Iterative fixes (for mixed type of mistype)
