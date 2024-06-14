
'''
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

tfidf_model = TfidfModel(corpus_bow, normalize=True)
index = SparseMatrixSimilarity(tfidf_model[corpus_bow], num_docs=len(corpus_bow), num_terms=len(dictionary))


query = "Polícia de Segurança Pública"
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


#perguntas = ["O quê?", "Como?", "Quando?", "Quem?", "Porquê?"]  #### por no ecrâ a perg 


for document in documents:
    id, document_id, timestamp, url, texto = document
    print(f"Documento ID: {document_id}")
    print(f"Texto: {texto}")
    print("-----------------------s---")
    
    for p in perguntas:
        result = question_answerer(question=p, context=texto)
        print(p)
        print(f"Score: {result['score']} | Resposta: {result['answer']}")
    print("\n")
'''


import json
from gensim.utils import tokenize
import nltk
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity
import sqlite3
from transformers import pipeline

# Baixar stopwords
nltk.download('stopwords')
stopwords = set(nltk.corpus.stopwords.words('portuguese'))

# Carregar dados do arquivo JSON
with open('drep.json', 'r') as file:
    data = json.load(file)

notes = [doc['notes'] for doc in data]

# Função para pré-processar o texto
def preprocess(line):
    line = line.lower()
    tokens = list(tokenize(line))
    tokens = [token for token in tokens if token not in stopwords]
    return tokens

# Pré-processar as notas
sentences = [preprocess(note) for note in notes]

# Criar dicionário e corpus
dictionary = Dictionary(sentences)
corpus_bow = [dictionary.doc2bow(sent) for sent in sentences]

# Treinar o modelo TF-IDF
tfidf_model = TfidfModel(corpus_bow, normalize=True)
index = SparseMatrixSimilarity(tfidf_model[corpus_bow], num_docs=len(corpus_bow), num_terms=len(dictionary))

# Consulta de exemplo
query = "Serviço de Informática da Polícia de Segurança Pública"
query_tokenized = preprocess(query)
query_bow = dictionary.doc2bow(query_tokenized)
tfidf_query = tfidf_model[query_bow]

# Calcular similaridades
sims = index[tfidf_query]
sims_ordered = sorted(enumerate(sims), key=lambda item: item[1], reverse=True)

# Caminho para o banco de dados
db_path = 'basededados.db'

# Função para buscar documentos pelo ID
def get_documents_by_ids(db_path, document_ids):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT * FROM dreapp_documenttext WHERE document_id IN ({})".format(','.join('?' for _ in document_ids))
    cursor.execute(query, document_ids)
    
    documents = cursor.fetchall()
    conn.close()
    return documents

# Selecionar os IDs dos documentos mais relevantes
num_documentos_mostrar = 5
document_ids = [data[idx]['id'] for idx, sim in sims_ordered[:num_documentos_mostrar]]

# Buscar os documentos no banco de dados
documents = get_documents_by_ids(db_path, document_ids)

# Configurar o modelo de Q&A com Llama-3-portuguese-Tom-cat-8b-instruct
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
model = AutoModelForCausalLM.from_pretrained("rhaymison/Llama-3-portuguese-Tom-cat-8b-instruct", device_map={"": 0})
tokenizer = AutoTokenizer.from_pretrained("rhaymison/Llama-3-portuguese-Tom-cat-8b-instruct")
model.eval()
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, do_sample=True, max_new_tokens=512, num_beams=2, temperature=0.3, top_k=50, top_p=0.95, early_stopping=True, pad_token_id=tokenizer.eos_token_id)

# Função para formatar o prompt
def format_prompt(question, context):
    system_prompt = "Abaixo está uma instrução que descreve uma tarefa, juntamente com uma entrada que fornece mais contexto. Escreva uma resposta que complete adequadamente o pedido."
    return f"{system_prompt}\n\nContexto: {context}\n\nPergunta: {question}\n\nResposta:"

# Conjunto de perguntas a serem feitas
perguntas = ["Onde?", "O quê?", "Como?", "Quando?", "Quem?"]

# Realizar Q&A em cada documento
for document in documents:
    id, document_id, timestamp, url, texto = document
    print(f"Documento ID: {document_id}")
    print(f"Texto: {texto}")
    print("--------------------------")
    
    for p in perguntas:
        prompt = format_prompt(p, texto)
        result = pipe(prompt)
        resposta = result[0]["generated_text"].split("Resposta:")[1].strip()
        print(p)
        print(f"Resposta: {resposta}")
    print("\n")
