import os
import json
import sqlite3
from gensim.utils import tokenize
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity
import nltk
from transformers import pipeline

# Baixar stopwords se necessário
nltk.download('stopwords')
stopwords = set(nltk.corpus.stopwords.words('portuguese'))

def preprocess(text):
    tokens = list(tokenize(text.lower()))
    tokens = [token for token in tokens if token not in stopwords]
    return tokens

def check_permissions(file_path):
    if os.access(file_path, os.R_OK) and os.access(file_path, os.W_OK):
        print(f"Permissões de leitura e escrita OK para: {file_path}")
    else:
        print(f"Problema de permissões com: {file_path}")
        raise PermissionError(f"Permissões inadequadas para o arquivo: {file_path}")

try:
    # Carregar os metadados do JSON
    with open('drep.json', 'r') as file:
        metadados = json.load(file)
    print("Metadados carregados com sucesso.")
    
    # Extrair os resumos (notes) e IDs dos documentos
    resumos = [doc['notes'] for doc in metadados]
    document_ids = [doc['id'] for doc in metadados]
    

    resumos_preprocessados = [preprocess(resumo) for resumo in resumos]
    print("Pré-processamento concluído.")
    
    dictionary = Dictionary(resumos_preprocessados)
    corpus = [dictionary.doc2bow(resumo) for resumo in resumos_preprocessados]
    print("Dicionário e corpus criados.")
    
    tfidf_model = TfidfModel(corpus)
    index = SparseMatrixSimilarity(tfidf_model[corpus], num_features=len(dictionary))
    print("Modelo TF-IDF treinado.")
    
    # Função para encontrar documentos relevantes
    def encontrar_documentos_relevantes(consulta, tfidf_model, index, dictionary, document_ids):
        consulta_preprocessada = preprocess(consulta)
        consulta_bow = dictionary.doc2bow(consulta_preprocessada)
        consulta_tfidf = tfidf_model[consulta_bow]
        similaridades = index[consulta_tfidf]
        documentos_relevantes = sorted(enumerate(similaridades), key=lambda item: item[1], reverse=True)
        return [(document_ids[idx], score) for idx, score in documentos_relevantes[:5]]
    
    def get_document_by_id(db_path, example_id):
        # Conectar à base de dados SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query para buscar o documento com o document_id fornecido
        query = "SELECT * FROM dreapp_documenttext WHERE document_id = ?"
        cursor.execute(query, (example_id,))
        
        # Obter o resultado da query
        document = cursor.fetchone()

        # Fechar a conexão
        conn.close()

        return document

    # Exemplo de consulta
    consulta = "Código da Contribuição Industrial"
    documentos_relevantes = encontrar_documentos_relevantes(consulta, tfidf_model, index, dictionary, document_ids)
    print(f"Documentos relevantes: {documentos_relevantes}")  # Mostrar os documentos relevantes

    db_path = 'basededados.db'  # Caminho para o seu banco de dados SQLite

    for doc in documentos_relevantes:
        doc_id, score = doc
        document_text = get_document_by_id(db_path, doc_id)
        id, document_id, timestamp, url, texto = document_text
        print(f"ID: {id}")
        print(f"Document ID: {document_id}")
        print(f"Timestamp: {timestamp}")
        print(f"URL: {url}")
        print(f"Texto: {texto}")
    else:
        print(f"Nenhum documento encontrado com o document_id = {document_id}")   



except Exception as e:
    print(f"Erro: {e}")