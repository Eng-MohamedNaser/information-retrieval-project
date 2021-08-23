import string
import nltk
import math
from tabulate import tabulate
#from tabulate import tabulate
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
#---------------------------------------------------
#functions
def cleaning(text):
    signs=[',','.','~','!','@','#','$','%','^','&','*','(',')','-','_','+','=',']','}','{','[','|','/','?','/t','/n',';','’','”','“','—']
    result = ""
    for char in text:
        if char not in signs:
         result = result+char
    return result.lower()
def removingStopWords(tokens):
    stopWords = stopwords.words('english')
    result =list()
    #print(stopWords)
    for token in tokens:
        if token not in stopWords:
         result.append(token)
    return result
def Stemmer(tokens):
    stemmer = PorterStemmer()
    result =list()
    #print(stopWords)
    for token in tokens:
        token=stemmer.stem(token)
        result.append(token)
    return result
def lemmetizer(tokens):
    stemmer = PorterStemmer()
    result =list()
    #print(stopWords)
    for token in tokens:
        token=stemmer.stem(token)
        result.append(token)
    return result
def preProcessing(fileNumber):
    f = open("C:/Users/Black user/Desktop/files/"+fileNumber+".txt", "r")
    test_text=f.read()
    f.close()
    #print("text :",test_text)
    #1-cleaning from singns
    cleanText=cleaning(test_text)
    print("clean text :",cleanText)
    #2-tokenize
    tokens=nltk.word_tokenize(cleanText)
    print("tokens :",tokens)
    #3-removing stop words
    afterRemoving=removingStopWords(tokens)
    print("without stop words :",afterRemoving)
    #4-stemmer
    afterStemmer=Stemmer(afterRemoving)
    print("after stemmer :",afterStemmer)
    return afterStemmer
def textPreProcessing(test_text):
    cleanText=cleaning(test_text)
    tokens=nltk.word_tokenize(cleanText)
    afterRemoving=removingStopWords(tokens)
    afterStemmer=Stemmer(afterRemoving)
    return afterStemmer
def creatingPostingIndex(postingList,finalTerms,fileNumber):
    #postingList = {}
    #finalTerms = preProcessing(str(fileNumber))
    pos = 0
    # l=creatingPostingIndex(postinList,n,1)
    for term in finalTerms:
        pos += 1
        if term in postingList:
            postingList[term][0] += 1
            if fileNumber in postingList[term][1]:
                postingList[term][1][fileNumber].append(pos)
            else:
                postingList[term][1][fileNumber] = []
                postingList[term][1][fileNumber].append(pos)
                #print(postingList)

        else:

            postingList[term] = []
            postingList[term].append(fileNumber)
            postingList[term].append({})
            postingList[term][0] = 0
            postingList[term][0] += 1
            if fileNumber in postingList[term][1]:
                postingList[term][1][fileNumber].append(pos)
            else:
                postingList[term][1][fileNumber] = []
                postingList[term][1][fileNumber].append(pos)
    return postingList
def all(numberOfFiles):

    counter=1
    postingIndex = {}
    for i in range(numberOfFiles):
        finaleTerms = preProcessing(str(counter))
        postingIndex=creatingPostingIndex(postingIndex,finaleTerms,counter)
        counter+=1

    return postingIndex
def phraseQuery(query,postingIndex):
    #pre processing to query
    queryPreProcessing=textPreProcessing(query)
    resultDec={}
    for term in queryPreProcessing:
        if term not in resultDec:
            if term in postingIndex:
                resultDec[term] = []
                resultDec[term].append(list(postingIndex[term][1]))
    #print(resultDec)
    matchedDocuments=[]

    if len(resultDec) >= 1:
        # for firest term
        for term in resultDec:
            matchedDocuments.append(resultDec[term][0])
            break
        #print("matched doc before removing ",matchedDocuments)
        # if more than 1 word
        #print("len of resultDec :",len(resultDec))
        #print(resultDec)
        if len(resultDec) >=2:
            #print(type(matchedDocuments))
            for doc in matchedDocuments:
                #print("matched doc is ",doc)
                for element in doc:
                    for term in resultDec:
                        doc = set(doc).intersection(resultDec[term][0])
                        matchedDocuments =list(doc)
    else:
        #print("no matched documents or stopword/s")
        return 0
    #print("Matched Documents for \"",query,"\" is :",matchedDocuments)
    return matchedDocuments
def getDF(query,postingIndex):
    result=phraseQuery(query,postingIndex)
    text=""
    if result==0:
        #print("no matched documents")
        return 0
    if len(result)==1:
        return len(result[0])
    else:return len(result)
def getTF(term,postingIndex,documentNumber):
    if documentNumber in postingIndex[term][1]:
        return len(postingIndex[term][1][documentNumber])
    else: return 0
def getTfWeight(term,postingIndex,documentNumber):
    tf=getTF(term,postingIndex,documentNumber)
    if tf==0:
        return 0
    else:
        return 1+math.log(tf)
def getIDF(term,postingIndex,n):
    df=getDF(term,postingIndex)
    if df==0:
        return 0
    return math.log(n/df)
def getTfIdf(term,postingIndex,n,documentNumber):
    tfWeight=getTfWeight(term,postingIndex,documentNumber)
    idf=getIDF(term,postingIndex,n)
    #print(tfWeight)
    #print(idf)
    if tfWeight==0:
        return 0
    return tfWeight*idf
def TfIdfMatrex(postingIndex,n):
    myData =[]
    for documentNumber in range(n):
        print("matrex for document number(",documentNumber+1,")")
        #myData=[]
        t=[]
        squares=0
        #to get document lenght
        for term in postingIndex:
            tf = round(getTF(term, postingIndex, documentNumber + 1), 2)
            tfWeight = round(getTfWeight(term, postingIndex, documentNumber + 1), 3)
            idf = round(getIDF(term, postingIndex, n), 3)
            if tfWeight == 0:
                idf = 0
            tfIdf = round(getTfIdf(term, postingIndex, n, documentNumber + 1), 3)
            if tfIdf!=0:
                squares += (tfIdf * tfIdf)
        Documentlenght = math.sqrt(squares)
        myData.append([documentNumber])
        #adding and printing
        for term in postingIndex:
            tf=round(getTF(term,postingIndex,documentNumber+1),2)
            tfWeight=round(getTfWeight(term,postingIndex,documentNumber+1),3)
            idf=round(getIDF(term,postingIndex,n),3)
            if tfWeight==0:
                idf=0
            tfIdf=round(getTfIdf(term,postingIndex,n,documentNumber+1),3)
            normalize=round(tfIdf/Documentlenght,3)
            t.append([term,tf,tfWeight,idf,tfIdf,normalize])
            myData[documentNumber].append(t)

        print("length for doc number",documentNumber+1,'=',Documentlenght)
        print("-------------------------+------+------------+-------+----------+--------------")
        print(tabulate(t, headers=['Term','TF','TFweight','IDF','TF-IDF','normalize'],tablefmt="orgtbl"))
        print("-------------------------+------+------------+-------+----------+--------------")
        print('\n\n')
    return myData
def getSimilarity(query,t1):

    postingIndex2={}
    #print(textPreProcessing(query))
    finalTerms=textPreProcessing(query)
    postingIndex2=creatingPostingIndex(postingIndex2,finalTerms,1)
    #print(postingIndex2)
    myData = []
    documentNumber=1
    squares=0
    t2=[]
    for term in postingIndex2:
        tf = round(getTF(term, postingIndex2, documentNumber), 2)
        tfWeight = round(getTfWeight(term, postingIndex2, documentNumber), 3)
        idf = round(getIDF(term, postingIndex2, n), 3)
        if tfWeight == 0:
            idf = 0
        tfIdf = round(getTfIdf(term, postingIndex2, n, documentNumber), 3)
        if tfIdf != 0:
            squares += (tfIdf * tfIdf)
    Documentlenght = math.sqrt(squares)
    # adding and printing
    for term in postingIndex2:
        tf = round(getTF(term, postingIndex2, documentNumber), 2)
        tfWeight = round(getTfWeight(term, postingIndex2, documentNumber), 3)
        idf = round(getIDF(term, postingIndex2, n), 3)
        if tfWeight == 0:
            idf = 0
        tfIdf = round(getTfIdf(term, postingIndex2, n, documentNumber), 3)
        normalize = round(tfIdf / Documentlenght, 3)
        t2.append([term, tf, tfWeight, idf, tfIdf, normalize])
        myData.append(t2)
    print("TF-IDF matrex for :",query )
    print(tabulate(t2, headers=['Term','TF','TFweight','IDF','TF-IDF','normalize'],tablefmt="orgtbl"))
    print('\n\n')
    for doc in range(len(t1)):
        similarity = 0
        for term2 in t2:
                for term in t1[doc][1]:
                    if term2[0]==term[0]:
                        #print('term1=',term,'\nterm2=',term2)
                        #print("found in doc",doc+1,"\nterm:",term[0],"=",term2[0])
                        #print(term[5],"*",term2[5])
                        similarity+= round(term[5]*term2[5],3)
                        #print("")
        similarity=round(similarity,3)
        print("similarity for doc",doc+1,'=',similarity)

#--------------------------------------------------------
#initialzing before start
n=10 #number of files
#---------------------------------------

#test case(1,2) : tokenization
fileNumber=1
preProcessing(str(fileNumber))

#test case(3) : posting index
# creating posting index for n files

#postingIndex=all(n)
#print(postingIndex)

#test case(4) : pharse query

#print("for book",phraseQuery("book",postingIndex))
#print("for development",phraseQuery("development",postingIndex))
#print("book and development",phraseQuery("book and development",postingIndex))

#test case(5) : TF

#term='program'
#documentNumber=1
#tf = getTF(term,postingIndex,documentNumber)
#print('TF for '+term+' in document',documentNumber,'=',tf)


#test case(6) : IDF

#idf = getIDF(term,postingIndex,n)
#print('IDF for '+term+'=',idf)


#test case (7)
#printig TF-IDF matrex for each file

#t1=TfIdfMatrex(postingIndex,n)


#test case (8)
#create TF-IDF table for query & finding similarity for eash document

#query="programming language Many of the designations used by manufacturers"
#getSimilarity(query,t1)