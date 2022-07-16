import jieba,xpinyin

temppinyin=xpinyin.Pinyin()
seg_list = list(jieba.cut("我杀了你妈"))
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
# print(list(seg_list))
# words_sentence=[]
# for i in seg_list:
#     if temppinyin.get_pinyin(i,splitter=" ")==i:
#         continue
#     words_sentence.append(temppinyin.get_pinyin(i,splitter=" "))

# print(words_sentence)