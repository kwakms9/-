from txt_util.file_op import read_file_utf8
from konlpy.tag import Kkma
import numpy as np
from txt_util.pos_tagging import tagging_no_tag
from txt_util.time_printer import print_time_msg
from sklearn.svm import LinearSVC, SVC
from tf_idf import duplicate_word_check,stop_word_checklist
clf = SVC(C=1, kernel='linear')
print_time_msg('time')

kkma = Kkma()#kkma=Kkma() okt먼저써보기
f = 'C:/Users/Me/Desktop/9000.csv'
stopwords = 'C:/Users/Me/Desktop/stopwordcom.csv'
lines = [line.split('#') for line in read_file_utf8(f).split('\r\n')[1:-1]]
labels = [line.split('#')[-1] for line in read_file_utf8(f).split('\r\n')[1:-1]]
stplist = [line for line in read_file_utf8(stopwords).split('\r\n')]

i = 0  # index
for line in lines:
   lines[i] = ' '.join(line[1:-1])
   i+=1

duplicate_word_check((lines))    #같은 문자 제거 lines의 주소값이 넘어감

morph = []
i=2
for line in lines:
    try:
        morph += [kkma.morphs(line)]
    except:
        print("error",i)
    #print(i) n use stopword 78%
    i+=1
print('m complete')


#stop_word_checklist(morph, stplist)
wset = []
for line in morph:
    for w in line:
        wset += [w]
wset = list(set(wset))
#print('wset size: ',len(wset),wset)
wordvec = np.zeros((len(lines),len(wset)))
sentlabel= np.array(labels)
lines.clear()
l = 0

for line in morph:
    for w in line:
        index = wset.index(w)
        wordvec[l][index]=1
        #print(wordvec[l])  #     백터완성ㅇ
    l+=1
i=0
#writvec=str(str(s)+'\n' for s in wordvec)

#for i in wordvec:
 #   writvec+=(str(i)+'\n')

#with open('binary.txt','w',encoding='utf8') as wf:
 # wf.write(writvec)
#print('kkk')
#input()
morph.clear()
wset.clear()
'''for label in labels:        #라벨 벡터
    sentlabel[i] = int(label)
    i+=1
    #print(i)'''
print('vec, label complete')
labels.clear()

trainsize = 8000

trainx = wordvec[:trainsize]
trainy = sentlabel[:trainsize]
print('x',len(trainx),'y',len(trainy))
testx = wordvec[trainsize:]
testy = sentlabel[trainsize:]
print('start fit')
print_time_msg('fit 시작')

clf.fit(trainx,trainy)
print_time_msg('끝')
print('fit finish')
#print_time_msg('predict 시작')
#print(clf.predict(testx))
#print_time_msg('끝')
#print(testy,'label')
print_time_msg('score 시작')
print(clf.score(testx,testy))
print_time_msg('끝')
