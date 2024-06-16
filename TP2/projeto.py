import json
from gensim.utils import tokenize
import nltk
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity
import sqlite3
from transformers import pipeline

nltk.download('stopwords')
stopwords = set(nltk.corpus.stopwords.words('portuguese'))

with open('drep.json', 'r') as file:
    data = json.load(file)

notes = [doc['notes'] for doc in data]

def preprocess(line):
    line = line.lower()
    tokens = list(tokenize(line))
    tokens = [token for token in tokens if token not in stopwords]
    return tokens


sentences = [preprocess(note) for note in notes]


dictionary = Dictionary(sentences)
corpus_bow = [dictionary.doc2bow(sent) for sent in sentences]

# Treinar o modelo TF-IDF
tfidf_model = TfidfModel(corpus_bow, normalize=True)
index = SparseMatrixSimilarity(tfidf_model[corpus_bow], num_docs=len(corpus_bow), num_terms=len(dictionary))


query = input("Digite a expressão que pretende pesquisar: ")
query_tokenized = preprocess(query)
query_bow = dictionary.doc2bow(query_tokenized)
tfidf_query = tfidf_model[query_bow]


sims = index[tfidf_query]
sims_ordered = sorted(enumerate(sims), key=lambda item: item[1], reverse=True)


db_path = 'basededados.db'


def get_documents_by_ids(db_path, document_ids):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT * FROM dreapp_documenttext WHERE document_id IN ({})".format(','.join('?' for _ in document_ids))
    cursor.execute(query, document_ids)
    
    documents = cursor.fetchall()
    conn.close()
    return documents


num_documentos_mostrar = 5
document_ids = [data[idx]['id'] for idx, sim in sims_ordered[:num_documentos_mostrar]]


documents = get_documents_by_ids(db_path, document_ids)


question_answerer = pipeline("question-answering", model="lfcc/bert-portuguese-squad")

user_choice = input("Deseja usar perguntas predefinidas (digite 'p') ou fornecer suas próprias perguntas (digite 'c')? ")

if user_choice.lower() == 'p':
    perguntas = ["O quê?", "Como?", "Quando?", "Quem?", "Porquê?"]
else:
    perguntas = []
    print("Digite suas perguntas uma por vez. Digite 'sair' para terminar.")
    while True:
        user_question = input("Digite sua pergunta: ")
        if user_question.lower() == 'sair':
            break
        perguntas.append(user_question)

for document in documents:
    id, document_id, timestamp, url, texto = document
    print(f"Documento ID: {document_id}")
    print(f"Texto: {texto}")
    print("--------------------------")
    
    for p in perguntas:
        result = question_answerer(question=p, context=texto)
        print(p)
        print(f"Score: {result['score']} | Resposta: {result['answer']}")
    print("\n")