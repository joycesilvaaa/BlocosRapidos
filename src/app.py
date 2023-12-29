from flask import Flask
import mysql.connector
from config import db_config

app = Flask(__name__)
app.secret_key = 'blocosrapidos'

from rotas import *

#Inicializa a conexão com o banco de dados
db_connection = mysql.connector.connect(**db_config)

#Cria um cursor para interagir com o banco de dados
cursor = db_connection.cursor()

#caminho para o arquivo sql
script_banco = 'banco.sql'

#funçao que executa o script
def criar_banco(script_banco):
    with open(script_banco, 'r') as script_file:
        script = script_file.read()
        cursor.execute(script)

if __name__ == "__main__":
    criar_banco(script_banco)
    app.run(debug=True)

