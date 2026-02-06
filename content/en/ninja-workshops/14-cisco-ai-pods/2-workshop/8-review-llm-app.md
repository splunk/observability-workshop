---
title: Review the LLM Application
linkTitle: 8. Review the LLM Application
weight: 8
time: 15 minutes
---

In the final step of the workshop, we'll deploy an application to our OpenShift cluster 
that uses the instruct and embeddings models. 

## What is LangChain? 

Like most applications that interact with LLMs, our application is written in Python.
It also uses [LangChain](https://www.langchain.com/), which is an open-source orchestration
framework that simplifies the development of applications powered by LLMs.

## Application Overview 

### Connect to the LLMs 

Our application starts by connecting to two LLMs that we'll be using: 

* `meta/llama-3.2-1b-instruct`: used for responding to user prompts 
* `nvidia/llama-3.2-nv-embedqa-1b-v2`: used to calculate embeddings 

``` python
# connect to a LLM NIM at the specified endpoint, specifying a specific model
llm = ChatNVIDIA(base_url=INSTRUCT_MODEL_URL, model="meta/llama-3.2-1b-instruct")

# Initialize and connect to a NeMo Retriever Text Embedding NIM (nvidia/llama-3.2-nv-embedqa-1b-v2)
embeddings_model = NVIDIAEmbeddings(model="nvidia/llama-3.2-nv-embedqa-1b-v2",
                                   base_url=EMBEDDINGS_MODEL_URL)
```
> Why are there two models? Here's a helpful analogy: 
> * The Embedding model is the "Librarian" (it helps find the right books), 
> * The Instruct model is the "Writer" (it reads the books and writes the answer).

### Define the Prompt Template

The application then defines a prompt template that will be used in interactions 
with the `meta/llama-3.2-1b-instruct` LLM: 

``` python
prompt = ChatPromptTemplate.from_messages([
    ("system",
        "You are a helpful and friendly AI!"
        "Your responses should be concise and no longer than two sentences."
        "Do not hallucinate. Say you don't know if you don't have this information."
        "Answer the question using only the context"
        "\n\nQuestion: {question}\n\nContext: {context}"
    ),
    ("user", "{question}")
])
```

> Note how we're explicitly instructing the LLM to just say it doesn't know the answer if 
> it doesn't know, which helps minimize hallucinations. There's also a placeholder for 
> us to provide context that the LLM can use to answer the question. 

### Connect to the Vector Database

The application then connects to the vector database that was pre-populated 
with NVIDIA data sheet documents: 

``` python
    weaviate_client = weaviate.connect_to_custom(
        http_host=os.getenv('WEAVIATE_HTTP_HOST'),
        http_port=os.getenv('WEAVIATE_HTTP_PORT'),
        http_secure=False,
        grpc_host=os.getenv('WEAVIATE_GRPC_HOST'),
        grpc_port=os.getenv('WEAVIATE_GRPC_PORT'),
        grpc_secure=False
    )
        
    vector_store = WeaviateVectorStore(
        client=weaviate_client,
        embedding=embeddings_model,
        index_name="CustomDocs",
        text_key="page_content"
    )
```

### Define the Chain

The application uses **LCEL (LangChain Expression Language)** to define the chain.
The `|` (pipe) symbol works like an assembly line; the output of one step becomes 
the input for the next.

``` python
    chain = (
        {
            "context": vector_store.as_retriever(),
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
```

Let's break this down step-by-step: 

* **Step 1: The Input Map {…}**: We are preparing the ingredients for our prompt.
  * context: We turn our vector store into a retriever. This acts like a search engine that finds the most relevant snippets from our NVIDIA data sheets based on the user’s question.
  * question: We use RunnablePassthrough() to ensure the user’s original question is passed directly into the prompt.
  * **Note**: These keys (context and question) map directly to the {context} and {question} placeholders we defined in our prompt template earlier.
* **Step 2: The prompt**: This is the instruction manual. It takes the context and the question and formats them using the prompt template (e.g., "Answer the question using only the context...").
* **Step 3: The llm**: This is the "Engine" (like GPT-4). It reads the formatted prompt and generates a response.
* **Step 4: The StrOutputParser()**: By default, AI models return complex objects. This "cleaner" ensures we get back a simple, readable string of text.

### Invoke the Chain

Finally, the application invokes the chain by passing the end user's question in 
as input: 

``` python
    response = chain.invoke(question)
```

This is the "Start" button. You drop the end users' question into the beginning of the pipeline, 
and it flows through the retriever, the prompt, and the LLM until the answer comes 
out the other side.