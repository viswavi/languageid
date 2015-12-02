#download random wikipedia articles using the Python Wikipedia library
#and perform some basic preprocessing
#requires reliable internet connection and may take 30 minutes

import wikipedia
import urllib2

languages = ['el', 'eo', 'en', 'zh', 'vi', 'ca', 'it', 'cs', 'ar', 'fi', 'eu', 'et', 'gl', 'id', 'es', 'ru', 'pt', 'no', 'tr', 'lt', 'vo', 'th', 'ro', 'pl', 'fr', 'bg', 'uk', 'sl', 'hr', 'de', 'ko', 'hu', 'fa', 'hi', 'nl', 'da', 'ja', 'he', 'ka', 'nn', 'sv', 'mk', 'sk', 'ms', 'sr']

for code in languages:
    wikipedia.set_lang(code)
    titles = wikipedia.random(1000)
    content = []
    for t in titles:
        try:
            body = wikipedia.page(t).content
            body = body.replace("==", " ")
            body = body.replace("\n", " ")
            print body
            content.append(body)
        except:
			body = ""
	file = open("testcorpus/" + code,'w')
	for c in content:
		file.write(c.encode('utf8') + " ")
	file.close()
    if(len(content) > 0):
        print content[0]	
