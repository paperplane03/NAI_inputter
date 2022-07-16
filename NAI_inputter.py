import os,pyperclip,xpinyin,pickle
import termcolor
from Parameter import *
import Viterbi_prefix

def welcome():
    print("Welcome to use NAI-inputter! Please input pinyin, or type \"HELP\" to get NAI help.")
    
def tutorial():
    print("PLEASE SEE THE **README** FILE-----!!!!!!")

def dealt_input():
    global stilled_list,now_pointer,waited_typelist
    # print(stilled_list)
    if stilled_list==[]:
        return
    waited_typelist=Viterbi_prefix.overall_viterbi(stilled_list)
    anslen=len(waited_typelist)
    if now_pointer>=anslen:
        now_pointer=0
    for ele in range(now_pointer,min(anslen,now_pointer+10)):
        print(str(ele)+" "+Viterbi_prefix.partial_sum(waited_typelist[ele])+" ",end="")
    print("")

def dealt_predict(char):
    global stilled_list,nowpre_pointer,waitedpre_typelist
    # print(stilled_list)
    if stilled_list!=[]:
        return
    waitedpre_typelist=Viterbi_prefix.predict_next(char)
    # print(waited_typelist)
    anslen=len(waitedpre_typelist)
    if nowpre_pointer>=anslen:
        nowpre_pointer=0
    print("PREDICT: ",end="")
    for ele in range(nowpre_pointer,min(anslen,nowpre_pointer+10)):
        print(str(ele)+" "+Viterbi_prefix.partial_sum(waitedpre_typelist[ele])+" ",end="")
    print("")

def input_process():
    global close_flag,buffer,stilled_list,now_pointer,waited_typelist,stilled_list,typedbuffer
    global nowpre_pointer
    temp_input=input()
    os.system("cls")
    if temp_input=="":
        pass
    elif temp_input=="Q":
        close_flag=1
    elif temp_input=="X":
        pyperclip.copy(typedbuffer)
    elif temp_input=="HELP":
        tutorial()
    elif temp_input[0]=="D":
        if temp_input=="DD":
            stilled_list=[]
            typedbuffer=""
            tempnum=0
        elif len(temp_input)>1:
            tempnum=int(temp_input[1:])
        else:
            # assert(0)
            tempnum=1
        if stilled_list!=[]:
            if len(stilled_list)>=tempnum:
                for j in range(tempnum):
                    stilled_list.pop()
                tempnum=0
                # stilled_list=stilled_list[0:len(stilled_list)-tempnum]
            else:
                tempnum-=len(stilled_list)
                stilled_list=[]
        if tempnum>0:
            if typedbuffer!="":
                if len(typedbuffer)>=tempnum:
                    typedbuffer=typedbuffer[0:len(typedbuffer)-tempnum]
            else:
                typedbuffer=""
        tempnum=0
        waited_typelist=[]
        now_pointer=0
        nowpre_pointer=0
        # os.system("cls")
        # if stilled_buffer!=[]:
        #     dealt_input()
        # pass
    elif temp_input[0]=="+":
        if stilled_buffer!=[]:
            if now_pointer+10<len(waited_typelist):
                now_pointer+=10
        else:
            if typedbuffer!="" and nowpre_pointer+10<len(waitedpre_typelist):
                nowpre_pointer+=10
    elif temp_input[0]=='-':
        if stilled_buffer!=[]:
            if now_pointer>0:
                now_pointer-=10
        else:
            if typedbuffer!="" and nowpre_pointer>0:
                nowpre_pointer-=10
        
    elif temp_input.isnumeric()==True:
        tempnum=int(temp_input)
        if stilled_list!=[]:
            if tempnum>=now_pointer and tempnum<max(now_pointer+10,len(waited_typelist)):
                choice=waited_typelist[tempnum]
                for i in range(len(choice)):
                    stilled_list.pop(0)
                typedbuffer+=Viterbi_prefix.partial_sum(choice)
        elif typedbuffer!="":
            if tempnum>=nowpre_pointer and tempnum<max(nowpre_pointer+10,len(waitedpre_typelist)):
                choice=waitedpre_typelist[tempnum]
                typedbuffer+=Viterbi_prefix.partial_sum(choice)
        now_pointer=0
        nowpre_pointer=0
    else:
        temp_output=Viterbi_prefix.cutupstring_enhence(temp_input)
        if temp_output==None:
            print("You inputted wrong pinyin! Please type right pinyin!")
        else:
            stilled_list+=temp_output
            now_pointer=0
            nowpre_pointer=0
        
        
    
def main_loop():
    global close_flag,buffer,stilled_list,typedbuffer
    
    while close_flag==0:

        # init print
        print("Buffer:",end="")
        for each_str in typedbuffer:
            if pinyinModule.get_pinyin(each_str)!=each_str:
                print(termcolor.colored(each_str,'blue'),end="")
        if stilled_list!=[]:
            for each_list in stilled_list:
                print("/"+termcolor.colored(each_list,'red'),end="")
            print("/",end="")
        print("")
        if stilled_list==[] and typedbuffer!="":
            # print("fhaowgfwai")
            dealt_predict(typedbuffer[-1])
        if stilled_list!=[]:
            dealt_input()
        input_process()

if __name__=="__main__":

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    Viterbi_prefix.read_chr()
    welcome()
    main_loop()