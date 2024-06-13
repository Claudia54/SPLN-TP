import json
from gensim.utils import tokenize
import nltk
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity
import sqlite3

nltk.download('stopwords')
stopwords = set(nltk.corpus.stopwords.words('portuguese'))

# Carregar dados do JSON
with open('drep.json', 'r') as file:
    data = json.load(file)

notes = [doc['notes'] for doc in data]

# Função de pré-processamento
def preprocess(line):
    line = line.lower()
    tokens = list(tokenize(line))
    tokens = [token for token in tokens if token not in stopwords]
    return tokens

# Pré-processar notas
sentences = [preprocess(note) for note in notes]

# Criar dicionário e corpus BoW
dictionary = Dictionary(sentences)
corpus_bow = [dictionary.doc2bow(sent) for sent in sentences]

# Criar modelo TF-IDF
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

db_path = 'basededados.db'  # Caminho para o seu banco de dados SQLite

def get_documents_by_ids(db_path, document_ids):
    # Conectar à base de dados SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query para buscar os documentos com os document_ids fornecidos
    query = "SELECT * FROM dreapp_documenttext WHERE document_id IN ({})".format(','.join('?' for _ in document_ids))
    cursor.execute(query, document_ids)
    
    # Obter os resultados da query
    documents = cursor.fetchall()

    # Fechar a conexão
    conn.close()

    return documents

# Obter IDs dos documentos mais similares
num_documentos_mostrar = 5
document_ids = [data[idx]['id'] for idx, sim in sims_ordered[:num_documentos_mostrar]]

# Buscar documentos completos em lote
documents = get_documents_by_ids(db_path, document_ids)

# Exibir resultados
for document in documents:
    id, document_id, timestamp, url, texto = document
    print(f"ID: {id}")
    print(f"Document ID: {document_id}")
    print(f"Timestamp: {timestamp}")
    print(f"URL: {url}")
    print(f"Texto: {texto}")
    print("\n")