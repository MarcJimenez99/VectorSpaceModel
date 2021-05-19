# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.
import sys
import parsing

arguments = len(sys.argv) - 1


position = 1

documentInfo = parsing.doc_docID_map 
termInfo = parsing.term_termID_map

if (arguments < 4):
    if (sys.argv[1] == "--doc"):
        print(f'Listing for document: {sys.argv[2]}')
        print(f'DOCID: {parsing.doc_docID_map[sys.argv[2]][0]}')
        print(f'Total terms: {parsing.doc_docID_map[sys.argv[2]][1]}')
    else:
        term = sys.argv[2]
        print(f'Listing for term: {sys.argv[2]}')
        print(f'TERMID: {parsing.term_termID_map[sys.argv[2]][0]}')
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
        print(f'Number of documents containing term: {doc_freq}')
        print(f'Term frequency in corpus: {parsing.term_termID_map[sys.argv[2]][1]}')
else:
    i = 0
    frequency = 0
    doc_positions = []
    docID = parsing.doc_docID_map[sys.argv[4]][0]
    term = sys.argv[2]
    print(f'Inverted list for term: {sys.argv[2]}')
    print(f'In document: {sys.argv[4]}')
    print(f'TERMID: {parsing.term_termID_map[sys.argv[2]][0]}')
    print(f'DOCID: {docID}')
    while (i < len(parsing.doc_dict[term])):
        tempID = parsing.doc_docID_map[parsing.doc_dict[term][i][0]][0]
        if tempID == docID:
            frequency += 1
            doc_positions.append(parsing.doc_dict[term][i][1])
        i += 1
    print(f'Term frequency in document: {frequency}')
    print(f'Positions: {doc_positions}')
 