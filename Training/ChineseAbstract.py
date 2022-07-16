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
huge_character={}
words_character={}
visited_character={}
def read_chr():
    global huge_character,words_character,visited_character
    if os.path.exists('huge_chara.pkl')==True:
        with open('huge_chara.pkl','rb') as pfile:
            huge_character=pickle.load(pfile)
    
    if os.path.exists('huge_words.pkl')==True:
        with open('huge_words.pkl','rb') as qfile:
            words_character=pickle.load(qfile)
   
    if os.path.exists('visited_words.pkl')==True:
        with open('visited_words.pkl','rb') as rfile:
            visited_character=pickle.load(rfile) 

def addkey(characters):
    if temppinyin.get_pinyin(characters)==characters:
        return
    global vo_idx,co_idx,huge_character
    now_pinyin=temppinyin.get_pinyin(characters)
    if now_pinyin!=characters:
        if doublevocheck(now_pinyin)==True:
            vo_idx=now_pinyin[0:2]
            co_idx=now_pinyin[2:]
        elif novocheck(now_pinyin)==True:
            vo_idx=''
            co_idx=now_pinyin
        else:
            vo_idx=now_pinyin[0]
            co_idx=now_pinyin[1:]
        # print(str(vo_idx)+" "+str(co_idx))
        try:
            vo_idx_num=index_vo.index(vo_idx)
            co_idx_num=index_co.index(co_idx)
        except:
            return
        huge_key=(vo_idx_num,co_idx_num)
        if huge_key not in huge_character:
            huge_character[huge_key]={}
        goal_dict=huge_character[huge_key]
        chara_ord=ord(characters)
        if chara_ord not in goal_dict:
            goal_dict[0]=1
            goal_dict[chara_ord]=1
        else:
            goal_dict[0]+=1
            goal_dict[chara_ord]+=1
    return

def wordsaddkey(characters):
    global temppinyin,words_character
    for ele in characters:
        if temppinyin.get_pinyin(ele)==ele:
            return
    now_pinyin=temppinyin.get_pinyin(characters,splitter="")
    # print(now_pinyin)
    if now_pinyin not in words_character:
        words_character[now_pinyin]={}
    goal_dict= words_character[now_pinyin]
    second_key=[]
    for ech in characters:
        second_key.append(ord(ech))
    second_key=tuple(second_key)
    if second_key not in goal_dict:
        goal_dict[0]=1
        goal_dict[second_key]=1
    else:
        goal_dict[0]+=1
        goal_dict[second_key]+=1
    return


'''Read the Files'''
read_chr()

for dic_num in range(65,78):
    dic_chr=chr(dic_num)
    # print(dic_chr)
    for file_num in range(100):
        print(dic_chr,file_num)
        if (dic_chr,file_num) in visited_character:
            continue
        else:
            visited_character[(dic_chr,file_num)]=1
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
                    sentences=re.split("，|。|？|！",eachtext)
                    # print(eachtext)
                    for characters in eachtext: 
                        addkey(characters)
                        # pass
                    for each_sentences in sentences: #用句号/分号拆成的分句
                        temp_segment=list(jieba.cut(each_sentences))
                        # print(temp_segment)
                        for ele in temp_segment:
                            wordsaddkey(ele)
                            # elepinyin=temppinyin.get_pinyin(ele,splitter='')
                            # words_character[elepinyin]
        
        fileopener=open("huge_chara.pkl",'wb')
        pickle.dump(huge_character,fileopener)
        fileopener.close()
        
        fileopener2=open("huge_words.pkl",'wb')
        pickle.dump(words_character,fileopener2)
        fileopener2.close()
        
        fileopener3=open("visited_words.pkl",'wb')
        pickle.dump(visited_character,fileopener3)
        fileopener3.close()
