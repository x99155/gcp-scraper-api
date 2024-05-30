from fastapi import FastAPI, HTTPException  
from pydantic import BaseModel  # Importation du module BaseModel de Pydantic pour la validation des données
from google.cloud import bigquery 
import os  # Importation du module os pour la gestion des variables d'environnement
from dotenv import load_dotenv  # Importation de load_dotenv pour charger les variables d'environnement depuis un fichier .env

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()

# Récupérer le chemin des credentials Google Cloud depuis les variables d'environnement
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Définir la variable d'environnement GOOGLE_APPLICATION_CREDENTIALS pour l'authentification avec Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

# Initialiser le client BigQuery
client = bigquery.Client()

# Créer une instance de l'application FastAPI
app = FastAPI()

# Définir un modèle de données pour les requêtes avec Pydantic
class QueryRequest(BaseModel):
    query: str  # La requête SQL à exécuter

# Définir une route POST pour exécuter une requête SQL
@app.post("/query")
async def execute_query(request: QueryRequest):
    try:
        # Exécuter la requête SQL
        query_job = client.query(request.query)
        results = query_job.result()  # Attendre la fin de l'exécution de la requête

        # Convertir les résultats en une liste de dictionnaires
        rows = [dict(row) for row in results]

        # Retourner les résultats sous forme de JSON
        return {"rows": rows}
    except Exception as e:
        # En cas d'erreur, lever une exception HTTP 500 avec le détail de l'erreur
        raise HTTPException(status_code=500, detail=str(e))



# Définir une route GET pour récupérer les données d'une table spécifique
@app.get("/table/{project_id}/{dataset_id}/{table_id}")
async def get_table_data(project_id: str, dataset_id: str, table_id: str):
    try:
        # Construire la requête SQL pour sélectionner toutes les lignes de la table spécifiée
        query = f"""SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"""
        
        # Exécuter la requête SQL
        query_job = client.query(query)
        results = query_job.result()

        # Convertir les résultats en une liste de dictionnaires
        rows = [dict(row) for row in results]

        # Retourner les résultats sous forme de JSON
        return {"rows": rows}
    except Exception as e:
        # En cas d'erreur, lever une exception HTTP 500 avec le détail de l'erreur
        raise HTTPException(status_code=500, detail=str(e))

# Point d'entrée principal pour lancer l'application FastAPI avec Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Lancer l'application sur l'hôte et le port spécifiés

