import sqlite3

conexao = sqlite3.connect("database.sqlite3")
cursor = conexao.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Empresa (
    Assai TEXT NOT NULL,
    Atacadão TEXT NOT NULL,
    Cometa Supermercados TEXT NOT NULL,
    Frangolandia TEXT NOT NULL,
    GBarbosa TEXT NOT NULL,
    Novo Atacarejo TEXT NOT NULL,
    Atakarejo TEXT NOT NULL
);
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS User (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    empresa_id INTEGER,
    FOREIGN KEY (empresa_id) REFERENCES Empresa(empresa_id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Estado (
    estado_id INTEGER PRIMARY KEY AUTOINCREMENT,
    estado TEXT NOT NULL,
    cidade TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Produto (
    produto_id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_nome TEXT NOT NULL,
    categoria TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Data_Inicio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_inicio TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Data_Fim (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_fim TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Preco (
    preco_id INTEGER PRIMARY KEY AUTOINCREMENT,
    preco_produto REAL,
    preco_validade TEXT,
    preco_app REAL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Campanha (
    campanha_id INTEGER PRIMARY KEY AUTOINCREMENT,
    campanha TEXT NOT NULL,
    data_campanha TEXT
);
''')

conexao.commit()
conexao.close()
