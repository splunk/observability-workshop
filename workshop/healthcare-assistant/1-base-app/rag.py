"""RAG retrieval for the healthcare assistant using PostgreSQL/pgvector."""
import asyncio
import os
from typing import Optional

from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from config import DOMAIN, load_config
from helpers.pgvector_utils import collection_exists, create_pgvector_store
from setup_env import setup_environment

_rag_cache = {}


class HealthcareRAGSystem:
    """RAG system with eager initialization."""

    def __init__(self, top_k: int = 5, model_name: Optional[str] = None):
        self.top_k = top_k
        self.model_name = model_name
        self.retrieval_chain = None
        self._initialized = False
        self.initialize()

    def initialize(self):
        if self._initialized:
            return

        try:
            app_config = load_config()
            rag_config = app_config.get("rag", {})
            vectorstore_config = app_config.get("vectorstore", {})
            model_config = app_config.get("model", {})

            embedding_model = vectorstore_config.get("embedding_model", "text-embedding-3-large")
            llm_model = (
                self.model_name
                or model_config.get("default_model")
                or model_config.get("model_name", "gpt-4o")
            )

            setup_environment()
            environment = os.environ.get("ENVIRONMENT", "local")

            if not os.environ.get("POSTGRES_PASSWORD"):
                raise ValueError(
                    "POSTGRES_PASSWORD not found. Please add it to .streamlit/secrets.toml"
                )

            if not collection_exists(DOMAIN, environment):
                collection_name = f"{DOMAIN}_{environment}_index"
                raise ValueError(
                    f"PostgreSQL collection not found: {collection_name}. "
                    f"Please run: python helpers/setup_vectordb.py {environment}"
                )

            embeddings = OpenAIEmbeddings(model=embedding_model)
            vector_store, _ = create_pgvector_store(embeddings, DOMAIN, environment)
            retriever = vector_store.as_retriever(search_kwargs={"k": self.top_k})

            llm = ChatOpenAI(
                model=llm_model,
                temperature=0.1,
                name="Healthcare RAG Assistant",
            )

            retrieval_qa_chat_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "Answer any use questions based solely on the context below:\n\n"
                        "<context>\n{context}\n</context>",
                    ),
                    MessagesPlaceholder("chat_history", optional=True),
                    ("human", "{input}"),
                ]
            )
            combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
            self.retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
            self._initialized = True
            print(f"✅ RAG system initialized (model: {llm_model})")
        except Exception as e:
            print(f"❌ Error initializing RAG system: {e}")
            import traceback

            traceback.print_exc()
            self._initialized = False

    async def search(self, query: str) -> str:
        if not self.retrieval_chain:
            return (
                "❌ RAG system not initialized. "
                "Please check your vector database setup."
            )

        try:
            result = await asyncio.to_thread(
                self.retrieval_chain.invoke, {"input": query}
            )
            return result["answer"]
        except Exception as e:
            return f"❌ Error during RAG search: {str(e)}"


def get_rag_system(top_k: int | None = None, model_name: Optional[str] = None) -> HealthcareRAGSystem:
    if top_k is None:
        app_config = load_config()
        top_k = app_config.get("rag", {}).get("top_k", 5)

    cache_key = f"{top_k}_{model_name or 'default'}"
    if cache_key not in _rag_cache:
        _rag_cache[cache_key] = HealthcareRAGSystem(top_k, model_name=model_name)
    return _rag_cache[cache_key]


def create_rag_tool(top_k: int | None = None, model_name: Optional[str] = None):
    """Create a LangChain retrieval chain tool for the agent."""
    rag_system = get_rag_system(top_k, model_name=model_name)

    @tool
    async def retrieve_healthcare_documents(query: str) -> str:
        """Retrieve information related to a query from the healthcare knowledge base."""
        return await rag_system.search(query)

    retrieve_healthcare_documents.name = "retrieve_healthcare_documents"
    retrieve_healthcare_documents.description = (
        "Retrieve information from the healthcare knowledge base"
    )
    return retrieve_healthcare_documents
