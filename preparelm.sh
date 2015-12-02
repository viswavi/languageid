for file in corpus/*
do
 cat $file |\
 python process.py |\
 ./KenLM/bin/lmplz -o 3 > $file.arpa
done
