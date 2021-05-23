import sys
import parsing
import re
import string
import math

query_map = {}
query_tfidf_map = {}
number_of_documents_in_corpus = (parsing.docID) - 1

with open(sys.argv[1]) as f:
    lines = [line.rstrip() for line in f]


def getQueryMap():
    for element in lines:
        for w in parsing.stop_list:
            pattern = r'\b'+w+r'\b'
            element = re.sub(pattern, '', element)
        query = element[element.find('Document'):].split()
        query = [''.join(c for c in s if c not in string.punctuation) for s in query]
        query = [s for s in query if s]
        query_no = element[:element.index('.')+len('.')]
        query_map[query_no] = query

def getDocumentInfo(document):
    return parsing.doc_docID_map[document][1]

def getTermFreqInDoc(term, document):
    i = 0
    frequency = 0
    docID = parsing.doc_docID_map[document][0]
    while (i < len(parsing.doc_dict[term])):
        tempID = parsing.doc_docID_map[parsing.doc_dict[term][i][0]][0]
        if tempID == docID:
            frequency += 1
        i += 1
    return frequency

def getDocFreq(term):
    i = 0
    doc_freq = 0
    while (i < len(parsing.doc_dict[term])):
        currentID = parsing.doc_docID_map[parsing.doc_dict[term][i][0]][0]
        if i == 0:
            doc_freq += 1
        else:
            prevID = parsing.doc_docID_map[parsing.doc_dict[term][i-1][0]][0]
            if currentID != prevID:
                doc_freq += 1
        i += 1
    return doc_freq

def get_query_TF_IDF():
    for key in query_map:
        i = 0
        queryTFIDF = []
        query = query_map[key]
        while(i < len(query)):
            currentTerm = query[i]
            if (getDocFreq(currentTerm) == 0):
                documentIDF = 0
            else:
                documentIDF = math.log(number_of_documents_in_corpus / getDocFreq(currentTerm))
            termfreq = 0
            for word in query:
                if(word is currentTerm):
                    termfreq += 1
            queryTF = termfreq / len(query)
            query_TFIDF = queryTF * documentIDF
            queryterm_tfIDF = (currentTerm, query_TFIDF)
            queryTFIDF.append(queryterm_tfIDF)
            i += 1

        query_tfidf_map[key] = queryTFIDF


def findTopTenDocuments(CoSim_scores_list):
    for list in CoSim_scores_list:
        list.sort(reverse=True, key=lambda x:x[1])
    
    return CoSim_scores_list

def outputToFile(CoSim_scores_map):
    resultsFile = open(sys.argv[2], "a")
    resultsFile.truncate(0)
    # <query−number>Q0<docno> <rank> <score>Exp
    i = 0
    for key in CoSim_scores_map:
        queryno = key
        listOfDocuments = CoSim_scores_map[queryno]
        rank = 0
        for element in listOfDocuments:
            docno = element[0]
            rank += 1
            score = element[1]
            if (rank < 11):
                str1 = f'{queryno[:-1]} {docno} {rank} {score} Exp\n'
                resultsFile.write(str1)
            else:
                break
    resultsFile.close()

def main():
    #Break down query_list.txt into dictionary
    getQueryMap()
    #Calculate TF_IDF for each query
    get_query_TF_IDF()
    #CoSim_scores_map holds the Cosine Similarity for each query and their respective documents
    CoSim_scores_map = {}
    #Holds the cosine similarity for a given query and all documents
    CoSim_scores_list = []

    #Iterates through each query in our query_tf_idf_map
        #Then iterates through each document and calculates cosine similarity
    for queryno in query_tfidf_map:
        query = query_tfidf_map[queryno]
        CoSim_document = []
        for docno in parsing.doc_docID_map:
            document_tfidf_list = []
            for tuple in query:
                term = tuple[0]
                termFreq = getTermFreqInDoc(term, docno)
                docFreq = getDocFreq(term)
                if (termFreq != 0):
                    if (docFreq == 0):
                        documentIDF = 0
                    else:
                        documentIDF = math.log(number_of_documents_in_corpus / docFreq)
                    docTF = termFreq / getDocumentInfo(docno)
                    doc_TFIDF = docTF * documentIDF
                    document_tfidf_list.append((term, doc_TFIDF))
                else:
                    document_tfidf_list.append((term, 0))
            if (len(document_tfidf_list) == 0):
                continue
            else:
                #Calculate the Cosine similarity
                query_values = []
                document_values = []
                for tuple in query:
                    for element in document_tfidf_list:
                        if (element[0] == tuple[0]):
                            query_values.append(tuple[1])
                            document_values.append(element[1])
                i = 0
                dotProduct = 0
                NormsOfQuery = 0
                NormsOfDoc = 0
                while (i < len(query_values)):
                    queryValue = query_values[i]
                    docValue = document_values[i]
                    product = (queryValue * docValue)
                    dotProduct += product

                    queryValueSquared = docValue * docValue
                    docValueSquared = queryValue * queryValue
                    NormsOfQuery += queryValueSquared
                    NormsOfDoc += docValueSquared
                    i += 1
                NormsOfQueryAndDoc = NormsOfQuery * NormsOfDoc
                NormsSqRoot = math.sqrt(NormsOfQueryAndDoc)
                if (NormsSqRoot != 0):
                    CoSimScore = dotProduct / NormsSqRoot
                    CoSimTuple = (docno, CoSimScore)
                    CoSim_document.append(CoSimTuple)
        CoSim_scores_list.append(CoSim_document)

    sortedList = findTopTenDocuments(CoSim_scores_list)
    increment = 0
    for queryno in query_tfidf_map:
        CoSim_scores_map[queryno] = sortedList[increment]
        increment += 1
    
    outputToFile(CoSim_scores_map) 

if __name__ == "__main__":
    main()

