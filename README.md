u# languageid
Identifying the language of input text using character-level n-grams, with support for 45 languages:
['Greek, Modern (1453-)', 'Esperanto', 'English', 'Chinese', 'Vietnamese', 'Catalan; Valencian', 'Italian', 'Volapuk', 'Czech', 'Arabic', 'Basque', 'Estonian', 'Galician', 'Indonesian', 'Spanish; Castilian', 'Russian', 'Dutch; Flemish', 'Portuguese', 'Norwegian', 'Turkish', 'Lithuanian', 'Thai', 'Romanian; Moldavian; Moldovan', 'Polish', 'French', 'Bulgarian   ', 'Malay', 'Croatian', 'German', 'Hungarian', 'Persian', 'Hindi', 'Finnish', 'Danish', 'Japanese', 'Hebrew', 'Georgian', 'Norwegian Nynorsk; Nynorsk, Norwegian', 'Serbian', 'Korean', 'Swedish', 'Macedonian', 'Slovak', 'Ukrainian', 'Slovenian']


This code implements character-level language models for each of these languages. This provides an estimated probability that a string belongs to each language.

The model's training data came from the  Multi-domain language identification dataset (Lui et al, 2011, http://people.eng.unimelb.edu.au/tbaldwin/). I wrote a script - extract.py - to randomly download Wikipedia articles, to use as test data. I lightly cleaned the data to remove html tags, removed non-dictionary English words (perceived to be proper nouns or part of the Wikipedia boilerplate), and removed English dictionary words from foreign corpora (which previously took more than 25% of tokens for smaller languages).

I used KenLM to create a 5-gram character-level language model, with modified Kneser-Ney smoothing. KenLM uses word n-grams, but a character-level language model is more suitable for for language identification. This becomes particularly important with languages like Chinese, Korean, and Japanese, so I trained the model on space-delimited characters and a special character representing whitespace. The models were produced as .arpa files and converted to binary for faster reading in Python.

The system has 4 basic components:
Data
  -data preprocessing in process_wikiraw.py
  -generating test corpus in extract.py
Training n-gram language models with KenLM
  -prepare-lm.py
Language Identification
  -core methods in train.py
  -test method in langid.py
Deployment
  -Deployed in Heroku via git

In order to test the system via web service:
if you wish to identify a string "हिन्दी विकिपीडिया", run
curl https://sheltered-chamber-9758.herokuapp.com/हिन्दी%20विकिपीडिया and you will see a response:
"(Hindi, 0.999)"

In order to build from scratch, in the Python REPL, try
from train import language
>> text = "Le parole est l\u0027ombre du fait"
>> print language(text)
...
>> ('en', 0.866)
