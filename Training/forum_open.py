import pickle
import os,re,json
import snownlp,jieba,xpinyin
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

temppinyin=xpinyin.Pinyin()

index_vo=['b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 'q', 'x', 'zh', 'ch', 'sh', 'r', 'z', 'c', 's', 'y', 'w', '']
index_co=['a', 'o', 'e', 'i', 'u', 'v', 'ai', 'ei', 'ui', 'ao', 'ou', 'uo', 'ia', 'iu', 'ie', 've', 'er', \
    'an', 'en', 'in', 'un', 'vn', 'ang', 'eng', 'ing', 'ong', 'ian', 'iang', 'iao', 'iong', 'ua', 'uan', 'uai', 'uang','ue']

huge_qa_character={}
words_qa_character={}
viterbi_qa_character={}
visit_qa_character={}

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

def read_chr():
    global huge_qa_character,words_qa_character,viterbi_qa_character,visit_qa_character
    if os.path.exists('huge_qa_chara.pkl')==True:
        with open('huge_qa_chara.pkl','rb') as pfile:
            huge_qa_character=pickle.load(pfile)
    
    if os.path.exists('huge_qa_words.pkl')==True:
        with open('huge_qa_words.pkl','rb') as qfile:
            words_qa_character=pickle.load(qfile)
   
    if os.path.exists('viterbi_qa_words.pkl')==True:
        with open('viterbi_qa_words.pkl','rb') as rfile:
            viterbi_qa_character=pickle.load(rfile) 
            
    if os.path.exists('visit_qa_words.pkl')==True:
        with open('visit_qa_words.pkl','rb') as sfile:
            visit_qa_character=pickle.load(sfile) 

def addkey(characters):
    if temppinyin.get_pinyin(characters)==characters:
        return
    global vo_idx,co_idx,huge_qa_character
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
        if huge_key not in huge_qa_character:
            huge_qa_character[huge_key]={}
        goal_dict=huge_qa_character[huge_key]
        chara_ord=ord(characters)
        if chara_ord not in goal_dict:
            goal_dict[0]=1
            goal_dict[chara_ord]=1
        else:
            goal_dict[0]+=1
            goal_dict[chara_ord]+=1
    return

def wordsaddkey(characters):
    global temppinyin,words_qa_character
    for ele in characters:
        if temppinyin.get_pinyin(ele)==ele:
            return
    now_pinyin=temppinyin.get_pinyin(characters,splitter="")
    # print(now_pinyin)
    if now_pinyin not in words_qa_character:
        words_qa_character[now_pinyin]={}
    goal_dict= words_qa_character[now_pinyin]
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

def viterbi_dictionary(characters:str,next_str:str or None,if_first=False):
    global vo_idx,co_idx,viterbi_qa_character
    if temppinyin.get_pinyin(characters)==characters:
        return
    if next_str!=None and temppinyin.get_pinyin(next_str)==next_str:
        return
    try:
        now_pinyin=temppinyin.get_pinyin(characters,splitter="")
        if now_pinyin not in viterbi_qa_character:
            viterbi_qa_character[now_pinyin]={}
        chrpinyin_dict=viterbi_qa_character[now_pinyin]
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
    
'''Read the Files'''
read_chr()


qa_list=[]
cnt=-1
with open('baike_qa_train.json',encoding='utf-8') as jsonf:
    for lines in jsonf.readlines():
        cnt+=1
        qa_list.append(json.loads(lines))
        if cnt%100==0:
            print(cnt)
        if cnt not in visit_qa_character:
            visit_qa_character[cnt]=1
        else:
            continue
        temp_strlist=qa_list[cnt]
        title_str=temp_strlist['title']
        desc_str=temp_strlist['desc']
        answer_str=temp_strlist['answer']
        
        title_text=re.split("\n",title_str)
        for eachtext in title_text:
            sentences=re.split("，|。|？|！|\?|\.|\!",eachtext)
            # print(eachtext)
            for characters in eachtext: 
                addkey(characters)
                # pass
            for each_sentences in sentences: #用句号/分号拆成的分句
                temp_segment=list(jieba.cut(each_sentences))
                # print(temp_segment)
                for ele in temp_segment:
                    wordsaddkey(ele)
            
            textlen=len(eachtext)
            for k in range(textlen):
                if k!=textlen-1:
                    viterbi_dictionary(eachtext[k],eachtext[k+1],k==0)
                else:
                    viterbi_dictionary(eachtext[k],None,k==0)
        
        
        desc_text=re.split("\n",desc_str)
        for eachtext in desc_text:
            sentences=re.split("，|。|？|！|\?|\.|\!",eachtext)
            # print(eachtext)
            for characters in eachtext: 
                addkey(characters)
                # pass
            for each_sentences in sentences: #用句号/分号拆成的分句
                temp_segment=list(jieba.cut(each_sentences))
                # print(temp_segment)
                for ele in temp_segment:
                    wordsaddkey(ele)
            
            textlen=len(eachtext)
            for k in range(textlen):
                if k!=textlen-1:
                    viterbi_dictionary(eachtext[k],eachtext[k+1],k==0)
                else:
                    viterbi_dictionary(eachtext[k],None,k==0)
                    
        
        answer_text=re.split("\n",answer_str)
        for eachtext in answer_text:
            sentences=re.split("，|。|？|！|\?|\.|\!",eachtext)
            # print(eachtext)
            for characters in eachtext: 
                addkey(characters)
                # pass
            for each_sentences in sentences: #用句号/分号拆成的分句
                temp_segment=list(jieba.cut(each_sentences))
                # print(temp_segment)
                for ele in temp_segment:
                    wordsaddkey(ele)
            
            textlen=len(eachtext)
            for k in range(textlen):
                if k!=textlen-1:
                    viterbi_dictionary(eachtext[k],eachtext[k+1],k==0)
                else:
                    viterbi_dictionary(eachtext[k],None,k==0)        
        
        fileopener=open("huge_qa_chara.pkl",'wb')
        pickle.dump(huge_qa_character,fileopener)
        fileopener.close()

        fileopener2=open("huge_qa_words.pkl",'wb')
        pickle.dump(words_qa_character,fileopener2)
        fileopener2.close()
        
        fileopener3=open("viterbi_qa_words.pkl",'wb')
        pickle.dump(viterbi_qa_character,fileopener3)
        fileopener3.close()
        
        fileopener4=open("visit_qa_words.pkl",'wb')
        pickle.dump(visit_qa_character,fileopener4) 
        fileopener4.close()
        if cnt%10000==9999:
            fileopener=open("huge_qa_chara"+str(cnt)+".pkl",'wb')
            pickle.dump(huge_qa_character,fileopener)
            fileopener.close()

            fileopener2=open("huge_qa_words"+str(cnt)+".pkl",'wb')
            pickle.dump(words_qa_character,fileopener2)
            fileopener2.close()
            
            fileopener3=open("viterbi_qa_words"+str(cnt)+".pkl",'wb')
            pickle.dump(viterbi_qa_character,fileopener3)
            fileopener3.close()
            
            fileopener4=open("visit_qa_words"+str(cnt)+".pkl",'wb')
            pickle.dump(visit_qa_character,fileopener4) 
            fileopener4.close()
        