from pymongo import MongoClient
import os

def get_conexao():
    # Troque pela URI do seu MongoDB Atlas depois
    MONGO_URI = os.getenv("MONGO_URI")
    client = MongoClient(MONGO_URI)
    return client['reconhecimento_facial']