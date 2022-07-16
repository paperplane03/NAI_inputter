from tkinter.messagebox import NO
import xpinyin,os,pickle,math
import snownlp,jieba

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

index_vo=['b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 'q', 'x', 'zh', 'ch', 'sh', 'r', 'z', 'c', 's', 'y', 'w', '']
index_co=['a', 'o', 'e', 'i', 'u', 'v', 'ai', 'ei', 'ui', 'ao', 'ou', 'uo', 'ia', 'iu', 'ie', 've', 'er', \
    'an', 'en', 'in', 'un', 'vn', 'ang', 'eng', 'ing', 'ong', 'ian', 'iang', 'iao', 'iong', 'ua', 'uan', 'uai', 'uang','ue']
cnt=0
temp_pinyinModule=xpinyin.Pinyin()

def doublevocheck(temp_str):
    if len(temp_str)<=1:
        return False
    if temp_str[1]=='h' and (temp_str[0]=='z' or temp_str[0]=='s' or temp_str[0]=='c'):
        return True
    return False

# print(doublevocheck("zhao"))

def novocheck(temp_str):
    if temp_str[0]=='a' or temp_str[0]=='e' or temp_str[0]=='i' or temp_str[0]=='o' or temp_str[0]=='u':
        return True
    return False

def pinyincheck(temp_str):
    if doublevocheck(temp_str)==True:
        vo_idx=temp_str[0:2]
        co_idx=temp_str[2:]
    elif novocheck(temp_str)==True:
        vo_idx=''
        co_idx=temp_str
    else:
        vo_idx=temp_str[0]
        co_idx=temp_str[1:]
    # print(str(vo_idx)+" "+str(co_idx))
    try:
        vo_idx_num=index_vo.index(vo_idx)
        co_idx_num=index_co.index(co_idx)
    except:
        return False
    return True



def read_chr():
    global huge_character,words_character
    if os.path.exists('huge_chara.pkl')==True:
        with open('huge_chara.pkl','rb') as pfile:
            huge_character=pickle.load(pfile)
    
    if os.path.exists('huge_words.pkl')==True:
        with open('huge_words.pkl','rb') as pfile:
            words_character=pickle.load(pfile)

def lookup_char(key1,key2):
    global huge_character
    if key1 not in huge_character:
        return None
    goal_dict=huge_character[key1]
    if key2 not in goal_dict:
        return None
    return goal_dict[key2]

def lookup_words(key1,key2):
    global words_character
    if key1 not in words_character:
        return None
    goal_dict=words_character[key1]
    if key2 not in goal_dict:
        return None
    return goal_dict[key2]

def cutupstring(input_str):
    str_len=len(input_str)
    nowcuts=-1
    temps=0
    ans=[]
    while nowcuts<str_len-1:
        temps=0
        for i in range(1,7):
            temp_str=input_str[nowcuts+1:nowcuts+1+i]
            if pinyincheck(temp_str)==True:
                temps=i
        if temps==0:
            return None
        ans.append(input_str[nowcuts+1:nowcuts+1+temps])
        nowcuts+=temps
    return ans
        
def all_True(temp_list:list):
    for i in temp_list:
        if i!=True:
            return False
    return True
    

def range_dp_method(input_list:list):
    global words_character
    strlen=len(input_list)
    # print(strlen)
    split=[[None for i in range(strlen)]for j in range(strlen)]
    dp_times=[[0 for i in range(strlen)]for j in range(strlen)]
    allstring=[["" for j in range(strlen)]for i in range(strlen)]
    for i in range(strlen):
        for j in range(i,strlen):
            tempstr=""
            for k in range(i,j+1):
                tempstr+=input_list[k]
            allstring[i][j]=tempstr
            
    for i in range(1,strlen+1):   #len
        for j in range(0,strlen-i+1): #range(j,j+i-1)
            # print("range:"+str(j)+" "+str(j+i-1))
            range_pinyin=allstring[j][j+i-1]
            if i==1:
                dp_times[j][j+i-1]=lookup_words(range_pinyin,0)
                # print(range_pinyin)
                # print(lookup_words(range_pinyin,0))
                split[j][j+i-1]=None
            else:
                for k in range(j,j+i): #(j,k)/(k+1,i+j-1)
                    if k!=j+i-1:
                        times1=dp_times[j][k]
                        times2=dp_times[k+1][i+j-1]
                        if times1==None or times2==None:
                            continue
                        if round(math.sqrt(times1*times2))>dp_times[j][i+j-1]:
                            # print(j,i+j-1,k)
                            dp_times[j][i+j-1]=round(math.sqrt(times1*times2))
                            split[j][i+j-1]=k
                    else:
                        if lookup_words(range_pinyin,0)!=None:
                            ptimes=lookup_words(range_pinyin,0)
                            if ptimes>=200:
                                dp_times[j][i+j-1]=ptimes*100
                                split[j][i+j-1]=None
    ans=[[0,strlen-1]]
    vis=[False]
    while all_True(vis)==False:
        for i in range(len(ans)):
            if vis[i]==False:
                if split[ans[i][0]][ans[i][1]]==None:
                    vis[i]=True
                else:
                    k=split[ans[i][0]][ans[i][1]]
                    ans.insert(i+1,[k+1,ans[i][1]])
                    ans[i][1]=k
                    vis.insert(i+1,False)
    ansstr=""
    for i in ans:
        temp_pinyin=allstring[i[0]][i[1]]
        backup_key=words_character[temp_pinyin][0]
        del words_character[temp_pinyin][0]
        temp_str=max(words_character[temp_pinyin],key=words_character[temp_pinyin].get)
        for j in temp_str:
            ansstr+=chr(j)
        # print(temp_str)
        words_character[temp_pinyin][0]=backup_key
    return ansstr

read_chr()
# temp_list=cutupstring("")
# print(range_dp_method(temp_list))
# print(words_character["xihuan"])
                        
                        
                