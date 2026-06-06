from flask import Flask, request, render_template, redirect, url_for, flash
from deepface import DeepFace
import numpy as np
import os
import projeto_repository

app = Flask(__name__)
# Chave secreta necessária para usar a função flash()
app.secret_key = 'super_chave_secreta_para_flash_messages'

# Garante que a pasta temp exista
os.makedirs("temp", exist_ok=True)

def calcular_distancia_cosseno(vetor1, vetor2):
    """Calcula a similaridade entre dois rostos."""
    v1 = np.array(vetor1)
    v2 = np.array(vetor2)
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return 1 - (dot_product / (norm_v1 * norm_v2))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    arquivo = request.files.get('imagem')

    if not nome or not arquivo:
        flash("Erro: Nome e imagem são obrigatórios!")
        return redirect(url_for('index'))

    caminho_temp = os.path.join("temp", arquivo.filename)
    arquivo.save(caminho_temp)

    try:
        # Extrai os dados do rosto usando o modelo Facenet
        dados_rosto = DeepFace.represent(img_path=caminho_temp, model_name="Facenet", enforce_detection=True)
        encoding = dados_rosto[0]["embedding"]
        
        # Salva usando nosso repositório
        projeto_repository.inserir_rosto(nome, encoding)
        
        os.remove(caminho_temp)
        flash(f"Sucesso! Rosto de {nome} cadastrado.")
    except Exception as e:
        if os.path.exists(caminho_temp): os.remove(caminho_temp)
        flash("Erro: Nenhum rosto detectado na imagem.")
    
    return redirect(url_for('index'))

@app.route('/reconhecer', methods=['POST'])
def reconhecer():
    arquivo = request.files.get('imagem')
    if not arquivo:
        flash("Erro: Imagem é obrigatória!")
        return redirect(url_for('index'))

    caminho_temp = os.path.join("temp", arquivo.filename)
    arquivo.save(caminho_temp)

    try:
        dados_rosto = DeepFace.represent(img_path=caminho_temp, model_name="Facenet", enforce_detection=True)
        encoding_alvo = dados_rosto[0]["embedding"]
        os.remove(caminho_temp)
        
        todos_rostos = projeto_repository.buscar_todos_rostos()
        
        melhor_match = None
        menor_distancia = 0.40 
        
        for rosto in todos_rostos:
            distancia = calcular_distancia_cosseno(encoding_alvo, rosto["encoding"])
            if distancia < menor_distancia:
                menor_distancia = distancia
                melhor_match = rosto["nome"]
                
        if melhor_match:
            flash(f"Rosto reconhecido: {melhor_match}")
        else:
            flash("Rosto não identificado ou desconhecido.")

    except Exception:
        if os.path.exists(caminho_temp): os.remove(caminho_temp)
        flash("Erro ao processar a imagem. Tente uma foto mais clara.")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)