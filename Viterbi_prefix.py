import math
import pickle
import os,re,copy
import snownlp,jieba,xpinyin
from Parameter import *
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


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

def pinyincheck_enhence(temp_str):
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
        return (False,None)
    return (True,vo_idx_num,co_idx_num)

def read_chr():
    global huge_character,words_character,associate_character
    
    if os.path.exists('./pkl/huge_chara.pkl')==True:
        with open('./pkl/huge_chara.pkl','rb') as pfile:
            huge_character=pickle.load(pfile)
    if os.path.exists('./pkl/huge_words.pkl')==True:
        with open('./pkl/huge_words.pkl','rb') as qfile:
            words_character=pickle.load(qfile)
    if os.path.exists('./pkl/viterbi.pkl')==True:
        with open('./pkl/viterbi.pkl','rb') as rfile:
            associate_character=pickle.load(rfile)

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


def cutupstring_enhence(input_str:str):
    global huge_character
    partial_pinyin=input_str.split("'")
    # print(partial_pinyin)
    ans=[]
    for every_part in partial_pinyin:
        str_len=len(every_part)
        nowcuts=-1
        temps=0
        while nowcuts<str_len-1:
            # print(nowcuts)
            temps=0
            for i in range(1,7):
                if nowcuts+i+1>str_len:
                    continue
                temp_str=every_part[nowcuts+1:nowcuts+1+i]
                pians=pinyincheck_enhence(temp_str)
                if pians[0]==True:
                    if (pians[1],pians[2]) in huge_character:
                        temps=i
            if temps==0:
                return None
            ans.append(every_part[nowcuts+1:nowcuts+1+temps])
            nowcuts+=temps
    return ans


'''Read the Files'''
# read_chr()

def viterbi(input_list:list):
    global associate_character
    inputlen=len(input_list)
    dp=[{} for i in range(inputlen)]
    comefrom=[{} for i in range(inputlen)]
    copys_dic=[{} for i in range(inputlen)]
    for i in range(inputlen):
        copys_dic[i]=copy.deepcopy(associate_character[input_list[i]])
        # print(copys_dic[i].keys())
        for eachkey in copys_dic[i].keys():
            dp[i][eachkey]=-10000
            comefrom[i][eachkey]=0
    tempsum=0
    for eachkey in copys_dic[0].keys():
        tempsum+=copys_dic[0][eachkey][0]
    for eachkey in copys_dic[0].keys():
        dp[0][eachkey]=math.log(copys_dic[0][eachkey][0]/tempsum)
        comefrom[0][eachkey]=eachkey
        
    for i in range(inputlen-1):
        tempsum=0
        for eachnowkey in dp[i].keys():
            # print(associate_character[input_list[i]][eachnowkey])
            temp_dict=associate_character[input_list[i]][eachnowkey]
            for eachnextkeys in dp[i+1].keys():
                if eachnextkeys not in temp_dict:
                    tempsum+=1
                else:
                    tempsum+=associate_character[input_list[i]][eachnowkey][eachnextkeys]
        for eachnowkey in dp[i].keys():
            tempdic=associate_character[input_list[i]][eachnowkey]
            for eachnextkeys in dp[i+1].keys():
                if eachnextkeys not in tempdic:
                    # print(chr(eachnowkey)+chr(eachnextkeys))
                    temppos=math.log(1/tempsum)
                else:
                    temppos=math.log(tempdic[eachnextkeys]/tempsum)
                if temppos+dp[i][eachnowkey]>dp[i+1][eachnextkeys]:
                    dp[i+1][eachnextkeys]=temppos+dp[i][eachnowkey]
                    comefrom[i+1][eachnextkeys]=eachnowkey

    backupans=[]
    pos_list=[]
    bestpos=-10000
    bestans=0
    for eachnowkey in dp[inputlen-1].keys():
        if dp[inputlen-1][eachnowkey]>bestpos:
            bestpos=dp[inputlen-1][eachnowkey]
            bestans=eachnowkey
    backupans.append(bestans)
    pos_list.append(bestpos)
    for eachnowkey in dp[inputlen-1].keys():
        if dp[inputlen-1][eachnowkey]>bestpos*0.75:
            backupans.append(eachnowkey)
            pos_list.append(dp[inputlen-1][eachnowkey])
    # print(bestans)
    # print(bestpos)
    backupanslen=len(backupans)
    ans=[[] for i in range(backupanslen)]
    for i in range(backupanslen):
        chain=backupans[i]
        ans[i].append(chain)
        for j in range(inputlen-1,0,-1):
            chain=comefrom[j][chain]
            ans[i].append(chain)
        ans[i].reverse()
        for j in range(len(ans[i])):
            ans[i][j]=chr(ans[i][j])
    return ans,pos_list

def partial_sum(temp_list,begin=-1,end=-1):
    partialsum=""
    if begin==-1:
        begin=0
    if end==-1:
        end=len(temp_list)
    for i in range(begin,end):
        partialsum+=temp_list[i]
    return partialsum

def overall_viterbi(input_list):
    ans_list=[]
    best_list,bestpos_list=viterbi(input_list)
    longest_ref=bestpos_list[0]
    ans_list+=best_list
    len1flag=0
    if len(input_list)==1:
        len1flag=1
        ans_list=[]
        input_list.append("")
    for i in reversed(range(len(input_list)-1)):
        tempsum=partial_sum(input_list,0,i+1)
        if tempsum in words_character:
            tempdict=words_character[tempsum]
            for ikey in reversed(dict(sorted(tempdict.items(),key=lambda x:x[1])).keys()):
                if ikey==0 or (ikey in ans_list):
                    continue
                if i!=0:
                    if tempdict[ikey]>=700:
                        tempele=[]
                        for j in ikey:
                            tempele.append(chr(j))
                        ans_list.append(tempele)
                else:
                    if tempdict[ikey]>=10:
                        tempele=[]
                        for j in ikey:
                            tempele.append(chr(j))
                        ans_list.append(tempele)
        else:
            tempchoice_list,tempchoicepos_list=viterbi(input_list[0:i+1])
            for j in range(len(tempchoicepos_list)):
                if tempchoicepos_list[j]>longest_ref*i/len(input_list)*1.2:
                    ans_list.append(tempchoice_list[j])
    if len1flag==1:
        input_list.pop()
    return ans_list

# print(huge_character)
read_chr()
# pinyin_list=cutupstring_enhence("ren'gongzhinengchengxusheji")
# print(pinyin_list)
# print(overall_viterbi(['ke']))

def predict_next(char):
    global associate_character
    char_pinyin=pinyinModule.get_pinyin(char)
    char_dic=associate_character[char_pinyin][ord(char)]
    anslist=[]
    for ikey in reversed(dict(sorted(char_dic.items(),key=lambda x:x[1])).keys()):
        if char_dic[ikey]>500 and ikey!=0 and ikey!=1 and ikey!=2:
            anslist.append(chr(ikey))
    return anslist
    # print(associate_character["ni"][ord('你')])
    
# print(predict_next('你'))