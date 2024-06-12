def add_table_schema(input_file, output_file):
    table_schema1 = """
    CREATE TABLE IF NOT EXISTS dreapp_document (
        id INTEGER,
        other_id INTEGER,
        tipo_documento TEXT,
        numero_documento TEXT,
        emissor TEXT,
        descricao TEXT,
        outro_campo TEXT,
        campo_booleano1 BOOLEAN,
        campo_booleano2 BOOLEAN,
        data_documento DATE,
        texto_longo TEXT,
        outro_campo2 TEXT,
        outro_campo3 TEXT,
        campo_booleano3 BOOLEAN,
        data_atualizacao TIMESTAMP,
        outro_campo4 BOOLEAN,
        outro_numero TEXT,
        outro_numero2 INTEGER,
        outro_numero3 TEXT
    );
    """
    
    table_schema2 = """
    CREATE TABLE IF NOT EXISTS dreapp_documenttext (
        id INTEGER,
        document_id INTEGER,
        timestamp TIMESTAMP,
        url TEXT,
        texto TEXT,
        primary key (id)
    );
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Escrever a estrutura da tabela dreapp_document e dreapp_documenttext
        outfile.write(table_schema1.strip() + '\n\n')
        outfile.write(table_schema2.strip() + '\n\n')
        # Escrever as consultas do arquivo original
        for line in infile:
            outfile.write(line)

# Exemplo de uso
input_file = 'filtered.sql'
output_file = 'filtered_with_schema.sql'
add_table_schema(input_file, output_file)
