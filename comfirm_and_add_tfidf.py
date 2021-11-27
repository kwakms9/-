

'''def refine(dictionary):       #없는 단어 저장후 다시 불러와야되서 함수로만듬
    #dictionary = ("D:\workspace\helloSC\wdictionary.csv")
    kdic = [line for line in read_file_utf8(dictionary).split('\r\n')[1:-1]] #bring dictionary
    #print(kdic,len(kdic))
    kdic = [line for line in kdic]

    for i in range(len(kdic)):  # 문자들 붙이기
        kdic[i] = ''.join(kdic[i])

    i = 0  # 인덱스
    j= 0 #,나온 횟수
    for line in kdic:  # ',,,,' <- 들이 모인것들을 인식 할수 있게 하기위해 split 할 것을 변경
        for k in range(1,len(kdic)+1):
            if ',' in line[-k] and j==1:
                line= line[:-k] + '#$#' + line[-k+1:]
                kdic[i]=line       #line 수정한것 추가
                j=0
                break
            elif ',' in line[-k]:
                line = line[:-k] + '#$#' + line[-k + 1:]
                j+=1
        i+=1

    kdic = [line.split('#$#') for line in kdic]     #classification

    return kdic

def wordnegpos(kdic):
    nepodic = {}    # neg, pos dic
    for i in range(len(kdic)):
        w = kdic[i][0]
        nepodic[w] = { 'Neg': kdic[i][1], 'Pos': kdic[i][2]}
    return nepodic'''

def duplicate_word_check(lines):    #중복제거
    i=0 #sent index
    for line in lines:
        limit = len(line)-1
        j=0 #word index
        while(j<limit):
            if line[j] == line[j+1]:#00 01 02 03 04 05 06  -7개     01 02 03 04 05 06 -6개 여야함
                line=line[:j]+line[j+1:]   #ex)12334 -> 12 + 34 ->1234
                limit-=1        #즁복제거 후 최대치 감소
            else:
                j+=1
            lines[i]=line
        i+=1

def stop_word_checkd(diction,stplist):    #불용어제거 딕션
    temp= diction.copy()
    for w in temp.keys():
        if str(w) not in stplist:
             pass
        else:
            del diction[w]

def stop_word_checklist(llist,stplist):    #불용어제거 리스트
    temp = []
    i=0
    for line in llist:
        temp = []
        for w in line:
            if str(w) not in stplist:
                temp += [w]
            else:
                pass
        llist[i] = temp
        i+=1

def compfirm_and_add_update(f,dictionary,stopwords):

    def tf_idf(lines):
        from sklearn.feature_extraction.text import TfidfVectorizer
        import numpy as np
        tt = TfidfVectorizer(min_df=1, tokenizer=kkma.morphs)
        tf = tt.fit_transform(lines)
        vocabs = tt.get_feature_names()
        worddic = {}
        word= str()
        temp=[]
        morphline=[]
        for i in range(len(lines)):
            value = ((''.join((str(tf[i])).split(' '))).split('\n'))
            value = [v.split('\t')[1] for v in value]
            print(value)
            for j in range(len(value)):
                index = np.nonzero(tf[i])[1][j]
                if ':' in value[j]: #오류? 불순물 제거
                    j+=1
                v = value[j]
                worddic[vocabs[index]] = v
                word=str(vocabs[index])
                temp+=[word]
            morphline += [temp]
            temp=[]
            i += 1
        print(worddic)
        return worddic,morphline

    from txt_util.file_op import read_file_utf8
    from konlpy.tag import Kkma
    from txt_util.pos_tagging import tagging_no_tag
    from txt_util.time_printer import print_time_msg
    print_time_msg('time')

    kkma = Kkma()#kkma=Kkma() okt먼저써보기
   # f = 'C:/Users/UTF8/Desktop/9000.csv'
    #lines = [line.split('#') for line in read_file_utf8(f).split('\r\n')[1:-1]]
    labels = [line.split('#')[-1] for line in read_file_utf8(f).split('\r\n')[1:-1]]
    stplist = [line for line in read_file_utf8(stopwords).split('\r\n')]

    i = 0  # index
   # for line in lines:
      #  lines[i] = ' '.join(line[1:-1])
     #   i+=1
    lines = ['좋았어요']
    duplicate_word_check((lines))    #같은 문자 제거 lines의 주소값이 넘어감
    tf_idf(lines)
    input()
    posline = []
    negline = []

    pos=0
    neg=0
    for i in range(len(labels)):  # pos,neg sentence set
        if '1' in labels[i]:
            posline += [lines[i]]
            pos+=1
        else:
            negline += [lines[i]]
            neg+=1
    print('pos',pos,'neg',neg)

        #print(posline)
        #print(labels)

        #posline += (morph[index] for index in posla[0])
        #negline += [morph[index] for index in negla[0]]

    posdic,posdicline = tf_idf(posline)   #positive valuse 일부 업뎃시 woflist 추가
    negdic,negdicline = tf_idf(negline)   #negative valuse 일부 업뎃시 woflist 추가

    stop_word_checkd(posdic,stplist)    #remove stopword
    stop_word_checkd(negdic,stplist)
    #print(negdic,posdic)
    #input()
    pos = 0
    neg = 0
    morph = []
    for i in range(len(labels)):  # pos,neg sentence set
        if '1' in labels[i]:
            morph += [posdicline[pos]]
            pos += 1
        else:
            morph += [negdicline[neg]]
            neg += 1

    stop_word_checklist(morph, stplist) #불용어 제거

    nepodic = {}
    for w in posdic.keys():  # pos neg 결합
        if w not in negdic.keys():
            negdic[w] = 0
    for w in negdic.keys():
        if w not in posdic.keys():
            posdic[w] = 0

    for w in posdic:
      nepodic[w] = {'Pos': posdic[w],'Neg': negdic[w]}

    return lines,morph,labels, nepodic