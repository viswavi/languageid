import subprocess, os

corpdir = os.path.dirname("/corpus/")

corp = set()

for root,dirs,files in os.walk(corpdir):
    for file in files:
       code = file[:2]
       corp.add(code)


corp = list(corp)

#for each file in '/corpus', create 5-gram character model, store as .arpa
#and then store as .binary for lightning-fast reading

for code in corp:
    cmd = "KenLM/bin/lmplz -o 5 --discount_fallback < corpus/" + code+ " > lm/" + code + ".arpa"
    status = subprocess.call(cmd, shell=True)
    cmd = "KenLM/bin/build_binary lm/" + code + ".arpa lm/" + code + ".binary"
    status = subprocess.call(cmd, shell=True)
