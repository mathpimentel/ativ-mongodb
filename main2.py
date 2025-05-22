# main.py
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["meu_banco"]
print(db.list_collection_names())

tarefa = {
    "titulo": "Fazer backup",
    "descricao": "Backup dos arquivos do servidor",
    "data_criacao": "2025-05-21",
    "status": "pendente"
}

# Suponha que essas variáveis sejam opcionais
tags = ["backup", "servidor"]
comentarios = [
    {"autor": "Ana", "mensagem": "Fazer antes das 18h", "data": "2025-05-21"}
]

# Adiciona tags se existirem e não estiverem vazias
if tags:
    tarefa["tags"] = tags

# Adiciona comentários se existirem e não estiverem vazios
if comentarios:
    tarefa["comentarios"] = comentarios
