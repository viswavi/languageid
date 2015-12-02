#!/usr/bin/env python
import os, sys, web, math, random, io, kenlm
#!/usr/bin/env python
from collections import defaultdict
import train

#remove qu, br, ht          or ( be, tl )

#remove qu, br, ht          or ( be, tl )
valid = train.valid
corp = train.corp
langs = dict(valid) 

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



'''
    def GET(self, name):
        results = train.language(models,name)
        return (langs[results[0]],results[1])
'''
models = map(lambda code: kenlm.LanguageModel('lm/' + code + ".binary"), corp)
persistent = ''
print train.language(models,"Le parole est l\u0027ombre du fait")

#!flask/bin/python
from flask import Flask

app = Flask(__name__)
    
@app.route('/language/<path:text>')
def index(text):
        valid = train.valid
        corp = train.corp
        models = map(lambda code: kenlm.LanguageModel('lm/' + code + ".binary"), corp)
        langs = dict(valid) 
        text = text.lower()
        results = train.language(models,text)
        persistent = results
        return "(" + langs[results[0]] + "," + str(results[1]) + ")"

if __name__ == '__main__':
    app.run(host='localhost',port=5000,debug=True)

'''
import web

urls = (
    '/(.*)', 'language'
)
app = web.application(urls, globals())

class language:        
    def GET(self, name):
        valid = train.valid
        corp = train.corp
        models = map(lambda code: kenlm.LanguageModel('lm/' + code + ".binary"), corp)
        langs = dict(valid) 
        name = name.lower()
        results = train.language(models,name)
        persistent = results
        return (langs[results[0]],results[1])

if __name__ == "__main__":
    app.run()   

    '''