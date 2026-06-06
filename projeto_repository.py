from conexao import get_conexao

db = get_conexao()
colecao_rostos = db['rostos']

def inserir_rosto(nome, encoding):
    colecao_rostos.insert_one({
        "nome": nome,
        "encoding": encoding
    })

def buscar_todos_rostos():
    return list(colecao_rostos.find())