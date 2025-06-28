import pinecone
import os
from dotenv import load_dotenv

load_dotenv()

pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment="gcp-starter")
index = pinecone.Index(os.getenv("PINECONE_INDEX_NAME"))

def store_user_data(user_id, vector, metadata=None):
    """
    Stores user data in Pinecone.
    :param user_id: Unique ID for the user
    :param vector: Embedding vector (list of floats)
    :param metadata: Optional dictionary of additional data
    """
    if metadata is None:
        metadata = {}

    index.upsert([(user_id, vector, metadata)])
