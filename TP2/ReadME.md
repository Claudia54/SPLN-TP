# Introduction

This project was created as part of Scripting and Natural Language Processing course. In this project, various aspects were explored through the construction of small exploratory programs that served as proof of concept.

# Data Processing

The file provided by the professor was processed and analyzed in the `clean_dre_dump.py` script. In this script, the `public` and `SET` statements were removed from the file, and the necessary table schemas for data storage were added. Finally, after cleaning the file, queries were executed to create an SQLite database.

# Information Retrieval (IR)

The `projeto.py` document describes the process of creating a text processing and document retrieval system. The system uses Natural Language Processing (NLP) techniques to preprocess textual data, train a TF-IDF model for document similarity, and implement a Question-Answering (Q&A) pipeline using a pre-trained language model. The goal is to retrieve relevant documents from a database based on a query and generate answers to predefined questions from these documents.

First, the data is loaded from a JSON file (`drep.json`). Each document in the dataset contains a `notes` field, which is the main text used for processing.

Text preprocessing involves converting the text to lowercase, tokenization, and removal of stopwords (common words that are filtered out). The `gensim.utils.tokenize` function is used for tokenization, and stopwords are removed using the NLTK library.

Next, a dictionary is created from the tokenized sentences, and a Bag-of-Words (BoW) corpus is generated. A TF-IDF model is trained using the BoW corpus, and a Sparse Matrix Similarity Index is created to calculate similarities between documents.

To process a query, the query text is preprocessed, converted to BoW, and transformed using the TF-IDF model. Similarities between the query and all documents are calculated and sorted in descending order.

The IDs of the most relevant documents are extracted, and these documents are retrieved from an SQLite database. For this, a function executes an SQL query on the database to select the documents by their IDs.

# Question and Answering (Q&A)

A pre-trained language model (`lfcc/bert-portuguese-squad`) is used to generate answers to predefined questions based on the content of the retrieved documents. For each document, a set of questions is posed, and the model generates answers based on the document's content.

The prompt for the model is formatted to provide the document context and the question to be answered. The model generates an answer for each question, which is then extracted and presented.

# Conclusion

This system combines Natural Language Processing (NLP) techniques and database manipulation to retrieve and analyze documents. It preprocesses textual data from a JSON file and trains a TF-IDF model to calculate similarities, identifying relevant documents in an SQLite database. It uses a pre-trained language model to generate answers based on the content of the retrieved documents. An additional script adjusts an SQL file for compatibility with SQLite and adds the necessary table schemas. This setup allows efficient information retrieval and contextual answer generation, facilitating the analysis of large volumes of textual data.
