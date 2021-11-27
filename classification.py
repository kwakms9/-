# -*- coding: utf-8 -*-
from txt_util.file_op import read_file_utf8
import numpy as np
from sklearn import svm
####################################현재 ' , ' 단위로 자르는 것으로 인한 문제발생=> 단위를 #단위로 바꿈
f ="C:/Users/UTF8/Desktop/ratings1.txt"
#lines = [line.split('#')[1] for line in read_file_utf8(f).split('\r\n')[1:-1]]#일반적인거
lines = [line.split('#') for line in read_file_utf8(f).split('\r\n')[1:-195000]]# #단위조금 손본거
i=0
for line in lines:
    line=' '.join(line[1:-1])
    lines[i]=line
    i+=1
    print(line)
lines = [line.split() for line in lines]
#print(lines,len(lines))
labels = [label.split('#')[-1] for label in read_file_utf8(f).split('\r\n')[1:-195000]]
print(labels,len(labels))
refinelabels=[]
refinelines=[]
intlabel = np.zeros(len(labels))
c=0
'''
for label in labels:
    #if '0' or '1' in label:
    if '0' in label or '1' in label:
        pass
    else:
        del lines[c]
        del labels[c]
    c+=1
#print(len(lines),len(labels))

for label in labels:
    for la in label[0]:
        if '0' in label or '1' in label:
            pass
        else:
            if('NAME?"' in label):
                 del lines[c]
                 del labels[c]
            else:
             i=3
             while('1' not in labels[c] and '0' not in labels[c]):
                ','.join(lines[c],labels[c:-1])
                print(lines[c])
        c+=1
print(len(lines),len(labels))
#print(labels)'''

intlabel = np.zeros(len(labels))    #line size
for i in range(len(labels)):
    intlabel[i]=int(labels[i])
#print(intlabel,type(intlabel))
words = []

for line in lines:
    words+=line        #insert

words = list(set(words))        #words set

vecarray = np.zeros((len(lines),len(words)))    #vector array

voca = {}
for line in lines:  #dictionary
    for w in line:
        if w in voca.keys():
            pass
        else:
            voca[w]=len(voca)

j = 0            #array index
for line in lines:
    for w in line:
        if w in voca.keys():
            i=voca[w]
            vecarray[j,i]=1
   # print(line)
   # print(vecarray[j])
    j+=1    #index rise

train_size = 5000
trainx =vecarray[:train_size]
testx = vecarray[train_size:]

trainy = intlabel[:train_size]
testy = intlabel[train_size:]
#print(type(testx),type(testy),len(vecarray),len(trainx),len(testx),len(intlabel),len(trainy),len(testy))
clf = svm.SVC()
clf.fit(trainx,trainy)
print('예상: ',clf.predict(testx))
print('답: ',testy)
print('적중률: ',clf.score(testx,testy))