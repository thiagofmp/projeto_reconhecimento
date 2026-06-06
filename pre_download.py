import os
from deepface import DeepFace

print("Iniciando download dos modelos...")
# Tentar carregar um modelo força o deepface a baixar os pesos
try:
    DeepFace.build_model("Facenet")
    print("Modelo Facenet baixado com sucesso!")
except Exception as e:
    print(f"Erro no download (pode ser memória): {e}")
