import re
import os
import zipfile
import string
from collections import defaultdict
from collections import OrderedDict

# Regular expressions to extract data from the corpus
doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)


with zipfile.ZipFile("data/ap89_collection_small.zip", 'r') as zip_ref:
    zip_ref.extractall()
   
# Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
    allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]

stop_list = []

doc_docID_map = {}
# docID_doc_map = {}
docID = 1

term_termID_map = {}
termID = 1

doc_dict = defaultdict(list)

punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''


with open("stopwords.txt", "r") as f:
    for line in f:
        stop_list.extend(line.split())

for file in allfiles:
    with open(file, 'r', encoding='ISO-8859-1') as f:
        filedata = f.read()
        result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents

        for document in result[0:]:
            # Retrieve contents of DOCNO tag
            docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
            # Retrieve contents of TEXT tag
            text = "".join(re.findall(text_regex, document))\
                      .replace("<TEXT>", "").replace("</TEXT>", "")\
                      .replace("\n", " ")
                      
            # step 1 - lower-case words, remove punctuation, remove stop-words, etc. 
            
            text = text.lower()
            text = text.translate(str.maketrans('', '', string.punctuation))

            for w in stop_list:
                pattern = r'\b'+w+r'\b'
                text = re.sub(pattern, '', text)
    
            # step 2 - create tokens 
            # step 3 - build index

            text = text.split()

            doc_str = ""
            doc_str = (docno).lower()
            position = 1
            for term in text:

                if term not in term_termID_map:  #if term unique
                    term_termID_map[term] = (termID, 1, 1) #(termid, termfreq overall in corpus, how many docs have this term)
                    termID += 1

                else: #if term is not unique
                    if term not in doc_dict: #if term is not unique to corpus and not unique in doc
                        term_termID_map[term] = (term_termID_map[term][0], term_termID_map[term][1] + 1, term_termID_map[term][2] + 1)
                    else: #if term is not unique to doc and corpus
                        term_termID_map[term] = (term_termID_map[term][0], term_termID_map[term][1] + 1, term_termID_map[term][2])

                if (term not in doc_dict):
                    doc_dict[term] = [(doc_str, position)]
                    position += 1
                else: 
                    doc_dict[term].append((doc_str, position))
                    position += 1 
                                

            doc_docID_map[doc_str] = (docID, len(text))
            # docID_doc_map[docID] = [doc_str]
            docID = docID + 1  

        