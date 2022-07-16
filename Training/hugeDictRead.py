import pickle
import os,re
import snownlp,jieba,xpinyin
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

huge_character={}
associate_character={}

def read_chr():
    global huge_character,words_character,associate_character
    
    if os.path.exists('huge_chara.pkl')==True:
        with open('huge_chara.pkl','rb') as pfile:
            huge_character=pickle.load(pfile)
    if os.path.exists('huge_words.pkl')==True:
        with open('huge_words.pkl','rb') as qfile:
            words_character=pickle.load(qfile)
    if os.path.exists('viterbi.pkl')==True:
        with open('viterbi.pkl','rb') as rfile:
            associate_character=pickle.load(rfile)
read_chr()

print(associate_character["hai"][28023][27915])
