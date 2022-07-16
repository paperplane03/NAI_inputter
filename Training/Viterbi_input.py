#Viterbi

import pickle
import os,re
import snownlp,jieba,xpinyin
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

file_prefix="./wiki_zh/A"
file_prefix2="/wiki_"
temppinyin=xpinyin.Pinyin()


index_vo=['b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 'q', 'x', 'zh', 'ch', 'sh', 'r', 'z', 'c', 's', 'y', 'w', '']
index_co=['a', 'o', 'e', 'i', 'u', 'v', 'ai', 'ei', 'ui', 'ao', 'ou', 'uo', 'ia', 'iu', 'ie', 've', 'er', \
    'an', 'en', 'in', 'un', 'vn', 'ang', 'eng', 'ing', 'ong', 'ian', 'iang', 'iao', 'iong', 'ua', 'uan', 'uai', 'uang','ue']
cnt=0

def doublevocheck(temp_str):
    if len(temp_str)<=1:
        return False
    if temp_str[1]=='h' and (temp_str[0]=='z' or temp_str[0]=='s' or temp_str[0]=='c'):
        return True
    return False

def novocheck(temp_str):
    if temp_str[0]=='a' or temp_str[0]=='e' or temp_str[0]=='i' or temp_str[0]=='o' or temp_str[0]=='u':
        return True
    return False

'''
Storing a huge dictionary 
'''

associate_character={}
# dict[0]:occur_times  dict[1]:occurs_at_first_times dict[2]:occur_at_last_times

def viterbi_dictionary(characters:str,next_str:str or None,if_first=False):
    if temppinyin.get_pinyin(characters)==characters:
        return
    if next_str!=None and temppinyin.get_pinyin(next_str)==next_str:
        return
    try:
        global vo_idx,co_idx,associate_character
        now_pinyin=temppinyin.get_pinyin(characters,splitter="")
        if now_pinyin not in associate_character:
            associate_character[now_pinyin]={}
        chrpinyin_dict= associate_character[now_pinyin]
        secondkey=ord(characters)
        if secondkey not in chrpinyin_dict:
            chrpinyin_dict[secondkey]={0:0,1:0,2:0}
        goal_dict=chrpinyin_dict[secondkey]
        goal_dict[0]+=1
        if if_first==True:
            goal_dict[1]+=1
        if next_str==None:
            goal_dict[2]+=1
        next_ord=ord(next_str)
        if next_ord not in goal_dict:
            goal_dict[next_ord]=0
        goal_dict[next_ord]+=1
        return
    except:
        return
    
def read_chr():
    global huge_character,words_character,associate_character
    if os.path.exists('viterbi.pkl')==True:
        with open('viterbi.pkl','rb') as pfile:
            associate_character=pickle.load(pfile)
# cnt=0  
'''Read the Files'''
read_chr()
templines=[]
for dic_num in range(65,78):
    dic_chr=chr(dic_num)
    print(dic_chr)
    for file_num in range(100):
        print(file_num)
        file_num_str="{0:02d}".format(file_num)
        templines=[]
        with open(file_prefix+dic_chr+file_prefix2+file_num_str,'r',encoding="utf-8") as process_f:
            for entries in process_f.readlines():
                templines.append(eval(entries))
                # print(len(templines))
            for j in templines:
                # print(j)
                text=j['text'].split("\n")
                text=[tempfor for tempfor in text if tempfor!='']
                # print(text)
                for eachtext in text:  # eachtext是每句话
                    print(eachtext)
                    sentences=re.split("，|。|？|！",eachtext)
                    textlen=len(eachtext)
                    for k in range(textlen):
                        if k!=textlen-1:
                            viterbi_dictionary(eachtext[k],eachtext[k+1],k==0)
                        else:
                            viterbi_dictionary(eachtext[k],None,k==0)
                            
            # print(templines)
# print(wordsaddkey["daxue"])
        # fileopener=open("viterbi.pkl",'wb')
        # pickle.dump(associate_character,fileopener)
        # fileopener.close()

