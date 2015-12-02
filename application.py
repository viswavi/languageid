#!/usr/bin/env python
import os, sys, web, math, random, io, kenlm
from collections import defaultdict
from flask import Flask
import train

#testing function, returning a dictionary where
# (k : (r,w)) in dictionary if of 1000 sentences from language k,
# r were classified accurately and w inaccurately
def test():
    counts = {}
    for c in corp:
        right = 0
        wrong = 0
        wrongs = defaultdict(int)
        text = io.open('testcorpus/' + c, encoding='utf-8').read()
        #because Chinese is logographic, so tokenizing by space is inappropriate
        text = text.split()
        for i in random.sample(range(1, len(text)-23), 1000):
            inds = map(lambda j: i + j, range(random.randint(1, 24)))
            randogram = map(lambda j: text[j], inds)
            ans = train.language(models, ' '.join(randogram))[0]
            if(ans != c): wrong += 1
            else: right += 1
            counts[c] = (right, wrong)
    return counts


#!flask/bin/python

app = Flask(__name__)

#example service call:
#ttp://localhost:8080/language/Le parole est l\u0027ombre du fait    
@app.route('/language/<path:text>')
def index(text):
         #compute dictionary of languages and codes for languages in the corpus
        valid = train.valid
        corp = train.corp
        #train models, by quickly reading .binary files
        models = map(lambda code: kenlm.LanguageModel('lm/' + code + ".binary"), corp)
        langs = dict(valid) 
        text = text.lower()
        results = train.language(models,text)
        persistent = results
        return "(" + langs[results[0]] + "," + str(results[1]) + ")"

if __name__ == '__main__':
    app.run(host='localhost',port=8080,debug=True)