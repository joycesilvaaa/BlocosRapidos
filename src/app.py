from flask import Flask
import mysql.connector
from config import db_config

app = Flask(__name__)

app.secret_key = 'blocosrapidos'

db_connection = mysql.connector.connect(**db_config)

def cria_tabelas_db():
    cursor = db_connection.cursor()
    comandos = [
        'USE BLOCOSRAPIDOS;',
        '''
        CREATE TABLE IF NOT EXISTS NOTAS(
            ID_NOTAS INT AUTO_INCREMENT PRIMARY KEY,
            TITULO_NOTAS VARCHAR(30) NOT NULL,
            CONTEUDO_NOTAS VARCHAR(1000) NULL,
            DATA_NOTA  DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        '''
    ]
    for comando in comandos:
        cursor.execute(comando)
    db_connection.commit()

from rotas import *

cria_tabelas_db()

if __name__ == "__main__":
    app.run(debug=True)

