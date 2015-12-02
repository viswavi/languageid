#to generate the wikipedia corpus into a directory called 'corpus',
#execute "python process_wikiraw.py"
#for fancier options with input, output, or formatting, use the cmd args

from collections import defaultdict
import os, io, enchant

import sys

#enter the corpus directory of the "Multi-domain language identification dataset"
if(len(sys.argv) == 1): diofrectory = "/home/vijay/Documents/jobs/yikyak/ijcnlp2011-langid/wikiraw/lang"
else: directory = sys.argv[1]	

if(len(sys.argv) >= 2): outdir = sys.argv[2]
else: outdir = "corpus"

#don't want to format the test corpus as space-delimited characters, in order to be realistic
if(len(sys.argv) >= 3 and sys.argv[3]=="noformat"): format = False
else: format = True

corpus = defaultdict(list)

for root,dirs,files in os.walk(directory):
    for file in files:
       code = file[:2]
       corpus[code].append(file)

eng = set()
for file in corpus['en']:
	g = io.open(directory + '/' + file, encoding='utf-8').read().split()
	for token in g:
		eng.add(token)

irreg = set()
#The English wikipedia has the most words, so identifying tokens not in
#the dictionary helps remove proper/technical nouns from other languages
dictionary = enchant.Dict("en_us")
for t in eng:
	if(not dictionary.check(t)):
		irreg.add(t)

#check for irregular noun from English wiki
def regular(token, lang):
	if token in irreg: return False
	if (token.startswith("[") or token.endswith("]") or token.endswith("].") or
		  	token.endswith("],")): return False
	if (token.startswith("{{") or token.endswith("}}") or token.endswith("}}.") or
		  	token.endswith("}},")): return False
	if (token[0]=='<' or token[-1]=='>'): return False
	#remove english words from other language corpora
	if(lang != 'en' and dictionary.check(token)): return False
	return True


for lang in corpus:
	#test file should be in unicode, train in utf-8
	if(outdir=='corpus'):
		f = io.open(outdir + '/' + lang, 'w', encoding='utf-8')
	else: f = io.open(outdir + '/' + lang, 'w')
	nums = len(corpus[lang])
	count = 0
	for file in corpus[lang]:
		if(outdir=='corpus'):
			g = io.open(directory + '/' + file, encoding='utf-8')
		else:
			g = io.open(directory + '/' + file)

		#convert all to lowercase, and tokenize by whitespace
		content = g.read().lower().split()
		#remove irregular nouns from the English pages
		content = filter(lambda t: regular(t,lang), content)
		if(content == []): continue
		if(format):
			#in order to train character-level language models with KenLM,
			#we need to delimit characters with spaces, and we replace 
			content = '#'.join(content)
			content = ''.join(content)
		f.write(' '.join(content) + "\n")
		g.close()
	f.close()	\