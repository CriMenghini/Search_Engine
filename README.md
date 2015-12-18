# Search_Engine
The purpuse of the project was to buil a Search Engine on a series of advertisements collected from websites of Kijiji. 
Given a specific query the Engine gives you back the documents that contains all the words in the query.
It was the first project of my life. When i wrote it ( in mid-november) it'd been just one month that i was programming. I built it in 2 weeks. It doesn't contain bugs, I mean, it works. But, actually, I think that there are many lines that may be dropped out, and many functions that could be rewritten.

# Structure of the project
It consists in three program that do different actions. 
- The collection: which with I collect the house's advertisements that contain the title of the article, the house description, it's price and location and some other infos.
- The index: after the pre-processing of the text, it makes an inverted index from which come up two files, the one is a posting list and the second the index.
- The search that includes the pre-processing of the query( the procedure is the same of the one apply to the articles), and the research of documents. In that part you would find the implementation of the intersection algorithm.

# Run the code
Once you are located in the folder which contains all the scripts:
- to retrieve the web pages run 
python Collect.py <min_kijiji><max_kijiji><min_imm><max_imm><min_att><max_att>
- min, max are the lower and the upper endpoints of the interval of pages to download respectiveli from www.kijiji.it, www.immobiliare.it, www.attico.it
- to build the index run
python Index.py
- to perform a query run
python Search.py

# More details
The following files are:
- Sites.txt contains the url bases of the retrieved web pages;
- Collect_lib.py is the library used by Collect program;
- Index_lib.py is the library used by Search program;
- Search_lib.py is the library used by Search program;

