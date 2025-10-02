import os
import weaviate
import logging

from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_weaviate import WeaviateVectorStore

# Read environment variables
DOCUMENT_URL = os.getenv('DOCUMENT_URL') # i.e. https://nvdam.widen.net/content/udc6mzrk7a/original/hpc-datasheet-sc23-h200-datasheet-3002446.pdf
EMBEDDINGS_MODEL_URL = os.getenv('EMBEDDINGS_MODEL_URL') # i.e. http://localhost:8001/v1

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"Loading data from {DOCUMENT_URL}")

try:
    # Load the specified PDF document
    loader = PyPDFLoader(
        DOCUMENT_URL
    )

    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    document_chunks = text_splitter.split_documents(documents)

    # Initialize and connect to a NeMo Retriever Text Embedding NIM (nvidia/llama-3.2-nv-embedqa-1b-v2)
    embeddings_model = NVIDIAEmbeddings(model="nvidia/llama-3.2-nv-embedqa-1b-v2",
                                       base_url=EMBEDDINGS_MODEL_URL)

    weaviate_client = weaviate.connect_to_custom(
        # url is:  http://weaviate.weaviate.svc.cluster.local:80
        http_host=os.getenv('WEAVIATE_HTTP_HOST'),
        http_port=os.getenv('WEAVIATE_HTTP_PORT'),
        http_secure=False,
        grpc_host=os.getenv('WEAVIATE_GRPC_HOST'),
        grpc_port=os.getenv('WEAVIATE_GRPC_PORT'),
        grpc_secure=False
    )

    db = WeaviateVectorStore.from_documents(
        documents=document_chunks,
        embedding=embeddings_model,
        client=weaviate_client,
        index_name="CustomDocs",
        text_key="page_content"
    )

except Exception as e:
    logger.error(f"Error loading data into Weaviate: {e}")

weaviate_client.close()