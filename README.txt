Index_creating.py

Creates inverted index file with a dictionary of stemmed words with their exact location in all the documents
Creates a file with a dictionary named processeddict with title, author and other parts separated under each document
Creates a file with dictionary named uncategorized_wordlist with list of words under each document

How to use:
1.Input the file path eg. C:\Python27\CranField
2.After the index creation a message is displayed "Index Created"
3.Run the search.py file to input the query

search.py

What it does?
1. Inputs the query
2. Preprocesses it
3. Displays the results with snippets 

How to use?
1. Run this file
2. Input the query. phrases should be enclosed by double quotes. if you dont want documents with a particular word , the syntax of the query should be !word
3. Type :q to quit



Additional features:
1.for the query ->   author 123
 author of the document number 123 will be returned

2.The output results display document number and all the snippers containing the query words. Top 25 results are displayed

3.boundary-layer is considered as boundary layer
