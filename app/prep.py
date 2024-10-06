import os
import requests
import pandas as pd
from sentence_transformers import SentenceTransformer
import minsearch2
from tqdm.auto import tqdm
from dotenv import load_dotenv

from db import init_db

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")
INDEX_NAME = os.getenv("INDEX_NAME")

BASE_URL = "https://raw.githubusercontent.com/PerisN/Healthcare-QandA-System/main"

def fetch_documents():
    print("Fetching documents...")
    relative_url = "data/data-with-ids.json"
    docs_url = f"{BASE_URL}/{relative_url}"
    docs_response = requests.get(docs_url)
    documents = docs_response.json()
    print(f"Fetched {len(documents)} documents")
    return documents

def fetch_ground_truth():
    print("Fetching ground truth data...")
    relative_url = "data/ground-truth-retrieval.csv"
    ground_truth_url = f"{BASE_URL}/{relative_url}"
    df_ground_truth = pd.read_csv(ground_truth_url)
    ground_truth = df_ground_truth.to_dict(orient="records")
    print(f"Fetched {len(ground_truth)} ground truth records")
    return ground_truth

def load_model():
    print(f"Loading model: {MODEL_NAME}")
    return SentenceTransformer(MODEL_NAME)

def index_documents(documents, model):
    print("Indexing documents...")
    
    text_fields = ['question_answer']
    keyword_fields = ['id']

    for doc in documents:
        doc['question_answer'] = doc['question'] + " " + doc['answer']
    index = minsearch2.Index(text_fields, keyword_fields)

    for doc in tqdm(documents, desc="Encoding documents"):
        for field in text_fields:
            doc[field] = model.encode(doc[field]).tolist()

    index.fit(documents)
    print(f"Indexed {len(documents)} documents")
    return index

def main():
    print("Starting the indexing process...")

    documents = fetch_documents()
    ground_truth = fetch_ground_truth()
    model = load_model()
    index = index_documents(documents, model)

    print("Initializing database...")
    init_db()

    print("Indexing process completed successfully!")

if __name__ == "__main__":
    main()