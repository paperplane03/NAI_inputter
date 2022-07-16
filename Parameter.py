import os,pyperclip,xpinyin,pickle
import termcolor

index_vo=['b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 'q', 'x', 'zh', 'ch', 'sh', 'r', 'z', 'c', 's', 'y', 'w', '']
index_co=['a', 'o', 'e', 'i', 'u', 'v', 'ai', 'ei', 'ui', 'ao', 'ou', 'uo', 'ia', 'iu', 'ie', 've', 'er', \
    'an', 'en', 'in', 'un', 'vn', 'ang', 'eng', 'ing', 'ong', 'ian', 'iang', 'iao', 'iong', 'ua', 'uan', 'uai', 'uang','ue']
buffer=""
typedbuffer=""
stilled_buffer=""
stilled_list=[]
close_flag=0
pinyinModule=xpinyin.Pinyin()
huge_character={}
words_character={}
associate_character={}
now_pointer=0
nowpre_pointer=0
waited_typelist=[]
waitedpre_typelist=[]