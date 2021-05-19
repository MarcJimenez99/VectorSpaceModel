# Each line of an output file should specify one retrieved document, in the following format:
# <query−number>Q0<docno> <rank> <score>Exp

# <query−number> is the number preceding the query in the query list
# <docno> is the document number, from the< DOCNO >field (which we asked you to index)
# <rank> is the document rank: an integer from 1-100
# <score> is the retrieval models matching score for the document
# Q0 and Exp are entered literally (because we will use a TREC evaluation code, so the output has to match exactly)

import parsing
import re
import string
import math

query_map = {}
query_tfidf_map = {}

doc_map = parsing.doc_docID_map
number_of_documents_in_corpus = (parsing.docID) - 1

with open('query_list.txt') as f:
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
            # print(f'Current Term: {currentTerm}')
            if (getDocFreq(currentTerm) == 0):
                documentIDF = 0
                # prelog = 0
            else:
                # prelog = number_of_documents_in_corpus / getDocFreq(currentTerm)
                documentIDF = math.log(number_of_documents_in_corpus / getDocFreq(currentTerm))
            # print(f'DocumentIDF: {number_of_documents_in_corpus} / {getDocFreq(currentTerm)} = {prelog} => log({documentIDF})')
            termfreq = 0
            for word in query:
                if(word is currentTerm):
                    termfreq += 1
            queryTF = termfreq / len(query)
            # print(f'QueryTF: {termfreq} / {len(query)} = {queryTF}')
            query_TFIDF = queryTF * documentIDF
            # print(f'QueryTFIDF: {queryTF} * {documentIDF} = {query_TFIDF}')
            queryterm_tfIDF = (currentTerm, query_TFIDF)
            # print(f'Term + TFIDF = {queryterm_tfIDF}')
            queryTFIDF.append(queryterm_tfIDF)
            i += 1

        query_tfidf_map[key] = queryTFIDF


def findTopTenDocuments(CoSim_scores_list):
    for list in CoSim_scores_list:
        list.sort(reverse=True, key=lambda x:x[1])
    
    return CoSim_scores_list

def outputToFile(CoSim_scores_map):
    resultsFile = open("results.txt", "a")
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

def main():
    getQueryMap()
    get_query_TF_IDF()

    CoSim_scores_map = {}
    CoSim_scores_list = []
    for queryno in query_tfidf_map:
        #list contains tuples = (docno, score)
        # CoSim_scores_list = []
        query = query_tfidf_map[queryno]
        # print(f'QueryNo: {queryno} | Query: {query}({len(query)})')
        # print(f'')
        CoSim_document = []
        for docno in parsing.doc_docID_map:
            # query = query_tfidf_map[queryno]
            document_tfidf_list = []
            for tuple in query:
                term = tuple[0]
                # print(f'term: {term}')
                termFreq = getTermFreqInDoc(term, docno)
                docFreq = getDocFreq(term)
                # print(f'termFreqInDoc: {termFreq}')
                # print(f'NumberOfDocumentsContainingTerm: {docFreq}')
                if (termFreq != 0):
                    if (docFreq == 0):
                        documentIDF = 0
                    else:
                        documentIDF = math.log(number_of_documents_in_corpus / docFreq)
                    docTF = termFreq / getDocumentInfo(docno)
                    # print(f'DOCTF: {termFreq} / {getDocumentInfo(docno)} = {docTF}')
                    doc_TFIDF = docTF * documentIDF
                    # print(f'DOCTFIDF: {docTF} * {documentIDF}')
                    document_tfidf_list.append((term, doc_TFIDF))
                else:
                    # continue
                    document_tfidf_list.append((term, 0))
            if (len(document_tfidf_list) == 0):
                continue
            else:
                #Calculate the Cosine similarity
                query_values = []
                document_values = []
                # print(f'PreQuery: {query}')
                # print(f'PreDoc: {document_tfidf_list}')
                for tuple in query:
                    for element in document_tfidf_list:
                        if (element[0] == tuple[0]):
                            # termFreq = getTermFreqInDoc(term, docno)
                            # docFreq = getDocFreq(term)
                            # print(f'Length Of Query: {len(query)} | Document Length: {getDocumentInfo(docno)} | Number of documents containing term: {docFreq} | Term frequency in document: {termFreq}')
                            # print(f'DocTerm: {element[0]} / QueryTerm: {tuple[0]}')
                            query_values.append(tuple[1])
                            document_values.append(element[1])
                
                # print(f'Query = {query_values}')
                # print(f'Document = {document_values}')
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
                # else:
                #     CoSimScore = 0 
                # CoSimTuple = (docno, CoSimScore)
                # CoSim_document.append(CoSimTuple)
            # print(f'Document {docno} Scores: {document_tfidf_list}')
        CoSim_scores_list.append(CoSim_document)

    sortedList = findTopTenDocuments(CoSim_scores_list)
    # print(sortedList)
    increment = 0
    for queryno in query_tfidf_map:
        CoSim_scores_map[queryno] = sortedList[increment]
        increment += 1
    
    outputToFile(CoSim_scores_map) 

    # print(CoSim_scores_map)
    # print(CoSim_scores_list)
    # print(f'Docs In Corpus: {number_of_documents_in_corpus}')
    # print(f'test: {math.log(0.55303)}')

if __name__ == "__main__":
    main()

