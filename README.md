# CS172 - Assignment 2 (Vector Space Model)

## Team member 1 - Marc Jimenez

###### Provide a short explanation of your design
For the assignment I used TF:IDF weights in order to calculate the Cosine Similarity between query and documents. First the code expects to receive two arguments in the form and order of **<Query_list>** and **<Output file>**. Next we will call our  **getQueryMap()** function to break down the **Query_list** file into a dictionary where the **queryno** acts as a key and and then call **getQuery_TF_IDF()** to then get the TF:IDF scores for each query. After that we will iterate through each **queryno** in our **query_tfidf_map** and get the Cosine Similiarity score for every document for the corresponding query. Finally **outputToFile()** will output the top 10 documents for each query in the given **Output file**. 
  
###### Language used, how to run your code, if you attempted the extra credit (stemming), etc. 
  
**Language Used:** Python 3.7.7
**How to run your code:** python VSM.py <Query_List> <Results File>
**Stemming/extra credit was not run originally in the Tokenizer created in Assignment 1.
