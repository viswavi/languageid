import os
from flask import Flask
import train

app = Flask(__name__)

@app.route('/<path:text>')
def hello(text):
#       return str(train.models[0].order)
        l = train.language(train.models, text)
        return "(" +l[0] + ", " + str(l[1]) + ")"
         #compute dictionary of languages and codes for languages in the corpus

