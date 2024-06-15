# Introdução
Este projeto foi criado no âmbito de Scripting e Processamento de Linguagem Natural.
Neste projeto explorou-se vários pontos, através da construção de pequenos programas  exploratórios que funcionaram  como prova de conceito.

# Processamento de Dados
Com o ficheiro que foi fornecido pelo professor foi processado e analisado no ficheiro clean_dre_dump.py. 
Neste script foram retirados os public e os SET do ficheiro e adicionados os esquemas das tabelas necessárias para o armazenamento dos dados. 
Finalmente, após a limpeza do ficheiro, são executadas as queries para a criação de uma base de dados SQLite.


# Information retrieval (IR)
No documento projeto.py descreve-se o processo de criação de um sistema de processamento de texto e recuperação de documentos. O sistema utiliza técnicas de Processamento de Linguagem Natural (PLN) para pré-processar dados textuais, treinar um modelo TF-IDF para similaridade de documentos e implementar um pipeline de Pergunta-Resposta (Q&A) usando um modelo de linguagem pré-treinado. O objetivo é recuperar documentos relevantes de um banco de dados com base em uma consulta e gerar respostas para perguntas predefinidas a partir desses documentos.

Primeiramente, os dados são carregados a partir de um arquivo JSON (drep.json). Cada documento no conjunto de dados contém um campo notes, que é o texto principal utilizado para processamento.

O pré-processamento do texto envolve a conversão do texto para minúsculas, tokenização e remoção de stopwords (palavras comuns que são filtradas). A função gensim.utils.tokenize é utilizada para a tokenização, e as stopwords são removidas usando a biblioteca NLTK.

Em seguida, é criado um dicionário a partir das sentenças tokenizadas, e um corpus Bag-of-Words (BoW) é gerado. Um modelo TF-IDF é treinado utilizando o corpus BoW, e um índice de Similaridade de Matriz Esparsa é criado para calcular as similaridades entre os documentos.

Para processar uma consulta, o texto da consulta é pré-processado, convertido para BoW e transformado usando o modelo TF-IDF. As similaridades entre a consulta e todos os documentos são calculadas e ordenadas em ordem decrescente.

Os IDs dos documentos mais relevantes são extraídos, e esses documentos são recuperados de um banco de dados SQLite. Para isso, é utilizada uma função que executa uma consulta SQL no banco de dados para selecionar os documentos pelos seus IDs.


# Question and Answering (Q&A)
Um modelo de linguagem pré-treinado (lfcc/bert-portuguese-squad) é utilizado para gerar respostas a perguntas predefinidas com base no conteúdo dos documentos recuperados. Para cada documento, um conjunto de perguntas é feito, e o modelo gera respostas baseadas no conteúdo do documento.

O prompt para o modelo é formatado de maneira que forneça o contexto do documento e a pergunta a ser respondida. O modelo gera uma resposta para cada pergunta, que é então extraída e apresentada.



# Conclusão 
Este sistema combina técnicas de Processamento de Linguagem Natural (PLN) e manipulação de banco de dados para recuperar e analisar documentos. Pré-processa dados textuais de um arquivo JSON e treina um modelo TF-IDF para calcular similaridades, identificando documentos relevantes em um banco de dados SQLite. Utiliza um modelo de linguagem pré-treinado para gerar respostas baseadas no conteúdo dos documentos recuperados. Um script adicional ajusta um arquivo SQL para compatibilidade com o SQLite e adiciona os esquemas de tabelas necessárias. Isso permite a recuperação eficiente de informações e a geração de respostas contextuais, facilitando a análise de grandes volumes de dados textuais.