**languageid**

Identifying the language of input text using character-level n-grams, with support for 45 languages:
['Greek, Modern (1453-)', 'Esperanto', 'English', 'Chinese', 'Vietnamese', 'Catalan; Valencian', 'Italian', 'Volapuk', 'Czech', 'Arabic', 'Basque', 'Estonian', 'Galician', 'Indonesian', 'Spanish; Castilian', 'Russian', 'Dutch; Flemish', 'Portuguese', 'Norwegian', 'Turkish', 'Lithuanian', 'Thai', 'Romanian; Moldavian; Moldovan', 'Polish', 'French', 'Bulgarian   ', 'Malay', 'Croatian', 'German', 'Hungarian', 'Persian', 'Hindi', 'Finnish', 'Danish', 'Japanese', 'Hebrew', 'Georgian', 'Norwegian Nynorsk; Nynorsk, Norwegian', 'Serbian', 'Korean', 'Swedish', 'Macedonian', 'Slovak', 'Ukrainian', 'Slovenian']


This code implements character-level language models for each of these languages. This provides an estimated probability that a string belongs to each language.

The model's training data came from the  Multi-domain language identification dataset (Lui et al, 2011, http://people.eng.unimelb.edu.au/tbaldwin/). I wrote a script - extract.py - to randomly download Wikipedia articles, to use as test data. I lightly cleaned the data to remove html tags, removed non-dictionary English words (perceived to be proper nouns or part of the Wikipedia boilerplate), and removed English dictionary words from foreign corpora (which previously took more than 25% of tokens for smaller languages).

I used KenLM to create a 5-gram character-level language model, with modified Kneser-Ney smoothing. KenLM uses word n-grams, but a character-level language model is more suitable for for language identification. This becomes particularly important with languages like Chinese, Korean, and Japanese, so I trained the model on space-delimited characters and a special character representing whitespace. The models were produced as .arpa files and converted to binary for faster reading in Python.

The system has 4 basic components:
*Data*
  -data preprocessing in process_wikiraw.py
  -generating test corpus in extract.py
*Training n-gram language models with KenLM*
  -prepare-lm.py
*Language Identification*
  -core methods in train.py
  -test method in langid.py
*Deployment*
  -Deployed in Heroku via git
br to test the system via web service:
if you wish to identify a string "हिन्दी विकिपीडिया", run
curl https://sheltered-chamber-9758.herokuapp.com/हिन्दी%20विकिपीडिया and you will see a response:
"(Hindi, 0.999)"

In order to build from scratch, in the Python REPL, try
from train import language
```
>> text = "Le parole est l\u0027ombre du fait"
>> print language(text)
...
>> ('en', 0.866)
```

*Accuracy and Testing*
For each language, I obtained 1000 random strings, averaging about 12 tokens per string (to be close to the size of the average Yak). For each sentence I identified the language automatically, and compared to the real language of origin to compute the accuracy. On average sentences were accurately identified 84.8% of the time, but widespread languages saw better results: English, French, German, and Hindi saw accuracy rates of 93.6, 92.4, 92.1, and 95.2%. The full results are as follows, in dictionary format where each key is (number correctly identified, number wrong) out of 1000.

{'el': (934, 66), 'eo': (862, 138), 'en': (936, 64), 'zh': (704, 296), 'vi': (918, 82), 'ca': (787, 213), 'it': (892, 108), 'vo': (960, 40), 'cs': (839, 161), 'ar': (958, 42), 'eu': (882, 118), 'et': (849, 151), 'gl': (641, 359), 'id': (773, 227), 'es': (882, 118), 'ru': (944, 56), 'nl': (862, 138), 'pt': (876, 124), 'no': (749, 251), 'tr': (855, 145), 'lt': (907, 93), 'th': (901, 99), 'ro': (868, 132), 'pl': (911, 89), 'fr': (924, 76), 'bg': (838, 162), 'ms': (477, 523), 'hr': (818, 182), 'de': (921, 79), 'hu': (897, 103), 'fa': (956, 44), 'hi': (952, 48), 'fi': (859, 141), 'da': (635, 365), 'ja': (875, 125), 'he': (931, 69), 'ka': (951, 49), 'nn': (593, 407), 'sr': (890, 110), 'ko': (911, 89), 'sv': (875, 125), 'mk': (802, 198), 'sk': (794, 206), 'uk': (912, 88), 'sl': (687, 313)}
