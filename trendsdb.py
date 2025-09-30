import chromadb
import pandas as pd
from chromadb.config import Settings

# Initialize ChromaDB client
# For persistent storage
client = chromadb.PersistentClient(path="./chroma_db")


# Create or get a collection
subtrends = client.get_or_create_collection(name="subtrends")

# Read CSV file
# df = pd.read_excel("Subtrendsref.xlsx")

# # Prepare data for ChromaDB
# documents = []  # Text content to be embedded
# metadatas = []  # Metadata for each document
# ids = []        # Unique IDs for each document

# for idx, row in df.iterrows():
#     # Combine text columns into a single document
#     # Adjust column names based on your CSV structure
#     doc_text = f"{row['description_en']} {row['label_en']}"
#     documents.append(doc_text)

#     # Store all other data as metadata
#     metadata = {
#         "key": str(row['key']),
#     }
#     metadatas.append(metadata)

#     # Create unique ID for each row
#     ids.append(f"row_{idx}")

# # Add documents to ChromaDB collection
# subtrends.add(
#     documents=documents,
#     metadatas=metadatas,
#     ids=ids
# )

# print(f"Added {len(documents)} documents to ChromaDB")


# results = subtrends.query(
#     query_texts=["what trends for Ai on business ?"],
#     n_results=5
# )

# print("\nQuery Results:")
# print(results)
