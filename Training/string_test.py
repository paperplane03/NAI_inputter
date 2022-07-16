import math
import pickle
import os,re,copy
import snownlp,jieba,xpinyin
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

index_vo=['b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 'q', 'x', 'zh', 'ch', 'sh', 'r', 'z', 'c', 's', 'y', 'w', '']
index_co=['a', 'o', 'e', 'i', 'u', 'v', 'ai', 'ei', 'ui', 'ao', 'ou', 'uo', 'ia', 'iu', 'ie', 've', 'er', \
    'an', 'en', 'in', 'un', 'vn', 'ang', 'eng', 'ing', 'ong', 'ian', 'iang', 'iao', 'iong', 'ua', 'uan', 'uai', 'uang','ue']

# near_pairs=[(q,a),(s,a),(z,a),(y,u),(h,u),(k,i),(l,o),(p,o),(w,e),(s,e),()]