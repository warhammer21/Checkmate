from langchain_openai import OpenAIEmbeddings
import os
import json
from tqdm import tqdm
import pandas as pd
# Initialize Pinecone
from pinecone import Pinecone, ServerlessSpec

pinecone = Pinecone(api_key="")
burger_index = pinecone.Index("burger-menu-index")
pizza_index = pinecone.Index("pizza-menu-index")

# Initialize OpenAI Embeddings
embed_model = OpenAIEmbeddings(model="text-embedding-ada-002",openai_api_key="")

def chunk_text(text, chunk_size=500):
    """
    Splits text into chunks of a specified size.
    """
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
def read_menu(file_path):
    """
    Reads a menu from a JSON file.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

# Replace with your file paths
burger_menu = read_menu("burger_menu.json")
pizza_menu = read_menu("pizza_menu.json")

def embed_and_upsert_menu(menu, index):
    """
    Embeds and upserts menu items into Pinecone index.
    """
    for category, items in menu.items():
        for item, options in items.items():
            # Prepare text for embedding
            text = f"{item}: {', '.join(options)}"
            ids = [item]
            texts = [text]
            embeds = embed_model.embed_documents(texts)
            metadata = [{
                "text": text,
                "title": item,
                "category": category
            }]
            index.upsert(vectors=zip(ids, embeds, metadata))

# Embed and upsert burger menu
# embed_and_upsert_menu(burger_menu, burger_index)
#
# # Embed and upsert pizza menu
# embed_and_upsert_menu(pizza_menu, pizza_index)
print(burger_index.describe_index_stats())
print(pizza_index.describe_index_stats())
