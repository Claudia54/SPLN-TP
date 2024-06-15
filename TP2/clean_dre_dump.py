import os
import re

def process_sql_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if not line.startswith('SET'):
                line = re.sub(r'INSERT INTO public\.(\w+)', r'INSERT INTO \1', line)
                outfile.write(line)

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

        outfile.write(table_schema1.strip() + '\n\n')
        outfile.write(table_schema2.strip() + '\n\n')

        for line in infile:
            outfile.write(line)

def remove_invalid_line(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if 'pg_catalog.set_config' not in line:
                outfile.write(line)

def execute_sqlite_command(sql_file, database):
    os.system(f"sqlite3 {database} < {sql_file}")

input_file = 'dre_dump.sql'
output_file = 'filtered_1.sql'
print("==================== Started process_sql_file ====================")
process_sql_file(input_file, output_file)

input_file = 'filtered_1.sql'
output_file = 'filtered_2.sql'
print("==================== Started add_table_schema ====================")
add_table_schema(input_file, output_file)

input_file = 'filtered_2.sql'
output_file = 'basededados.sql'
print("==================== Started remove_invalid_line ====================")
remove_invalid_line(input_file, output_file)

input_file = 'database.sql'
output_file = 'database.db'
print("==================== Started execute_sqlite_command ====================")
execute_sqlite_command(input_file, output_file)
