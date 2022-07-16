import os,pickle

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def read_chr():
    global huge_character,words_character
    if os.path.exists('huge_chara.pkl')==True:
        with open('huge_chara.pkl','rb') as pfile:
            huge_character=pickle.load(pfile)
    
    if os.path.exists('huge_words.pkl')==True:
        with open('huge_words.pkl','rb') as pfile:
            words_character=pickle.load(pfile)
read_chr()
print(words_character["xi"])
