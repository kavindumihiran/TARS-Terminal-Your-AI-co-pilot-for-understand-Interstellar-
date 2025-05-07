import os 
import streamlit as st

from haystack import version 
from haystack import Pipeline
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.converters import HTMLToDocument
from haystack.components.writers import DocumentWriter
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import ChatPromptBuilder
from haystack.components.generators.utils import print_streaming_chunk

from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack_integrations.components.embedders.mistral.document_embedder import MistralDocumentEmbedder
from haystack_integrations.components.embedders.mistral.text_embedder import MistralTextEmbedder
from haystack_integrations.components.generators.mistral import MistralChatGenerator

os.environ["MISTRAL_API_KEY"] = "YOUR_API_KEY"

document_store = InMemoryDocumentStore()
fetcher = LinkContentFetcher()
converter = HTMLToDocument()
embedder = MistralDocumentEmbedder()
writer = DocumentWriter(document_store=document_store)

splitter = DocumentSplitter(split_by="word", split_length=400, split_overlap=50)

indexing = Pipeline()

indexing.add_component("fetching", LinkContentFetcher())                                 # Fetch the raw HTML from the URL
indexing.add_component("Converter", HTMLToDocument())                                    # Get a readable document from the raw HTML data
indexing.add_component("splitter", splitter)                                             # split the document into chunks before embedding done 
indexing.add_component("embedder", MistralDocumentEmbedder())                            # Embedd the document
indexing.add_component("writer", DocumentWriter(document_store=document_store))          # Store the embedded document in memory

# in this each component has only one input and output and in each stage the previous output becomes the input to the next stage. No external arguments or inputs needed during the middle stages of the pipeline 
indexing.connect("fetching", "Converter")       # connect the component and create the complete pipeline
indexing.connect("Converter", "splitter")
indexing.connect("splitter", "embedder")       # Fetching --> Converter --> splitter --> Embedding --> Writer
indexing.connect("embedder", "writer")

# When selecting URLs you need to be carefull to add the relevant sites and the information should be quality

urls = ["https://www.imdb.com/title/tt0816692/ratings/?ref_=tturv_sa_3",
        "https://www.imdb.com/title/tt0816692/fullcredits/?ref_=tt_cst_sm",
        "https://en.wikipedia.org/wiki/Interstellar_(film)#Music",
        "https://www.imdb.com/title/tt0816692/awards/?ref_=tturv_sa_1"]

indexing.run({"fetching": {"urls": urls}}) # You only need to give the first stage of the pipeline. And it will run because no inputs or arguments needed in the middle of the pipeline.

from haystack.dataclasses import ChatMessage

chat_template = """
                {% if documents %}
                Answer based on the provided context only. Be precise and factual.
                Question: {{query}}
                Context:
                {% for doc in documents %}
                - {{doc.content}}
                {% endfor %}
                Answer:
                {% else %}
                No relevant documents found.
                {% endif %}
                """

user_message = ChatMessage.from_user(chat_template) # We need to give the LLM a promt that is similar to a user given promt. This line ensure the promt is like a user given promt while ensuring our template.

text_embedder = MistralTextEmbedder()  # embedd the question that the user askes from the RAG with tha same embedding that we use before 
retriver = InMemoryEmbeddingRetriever(document_store=document_store, top_k=3)  # Retrieve the top similar document to the question, The embedded documents are in the document_store.
prompt_builder = ChatPromptBuilder(template=user_message, variables=["query", "documents"], required_variables=["query", "documents"]) # bulids the prompt using the template given before, to give to the LLM 
generator = MistralChatGenerator(model='mistral-medium', streaming_callback=print_streaming_chunk)  # This parameter is used to stream the LLM output in real-time while the model is generating the answer.

rag_pipeline = Pipeline()
rag_pipeline.add_component("text_embedder", text_embedder)
rag_pipeline.add_component("retriver", retriver)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("generator", generator)

# In this pipeline stages there are multiple inputs and outputs, Thats why we use "text_embedder.embedding" to get the relevant output of that stage. Same for the inputs also.
rag_pipeline.connect("text_embedder.embedding", "retriver.query_embedding")
rag_pipeline.connect("retriver.documents", "prompt_builder.documents")         # Question --> Embedding --> Retrieveing similar docs --> Buiding the prompt --> Generate the answer using LLM
rag_pipeline.connect("prompt_builder.prompt", "generator.messages")

st.set_page_config(page_title="TARS Terminal")

# Background Image Styling
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://wallpaperaccess.com/full/2786392.jpg');
        background-size: cover;
        background-position: center;
        opacity: 1;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌌 TARS Terminal")
st.write("Your AI co-pilot through the cosmos of *Interstellar* — 90% sarcasm, 100% accuracy.")

user_query = st.text_input("Your question", placeholder="e.g :- Who directed the movie", key="input")

submit = st.button("Ask")

if submit and user_query:
    with st.spinner("Generating the answer"):

        message = [ChatMessage.from_user(chat_template)]

        results = rag_pipeline.run(        # In this RAG pipeline each stages need specific arguments/inputs, Thats why we cannot just past the first stage as in the indexing pipeline. 
            {
                "text_embedder": {"text": user_query},
                "prompt_builder": {"template": message, "query": user_query},
                "generator": {"generation_kwargs": {"max_tokens": 1000}}
            },
            include_outputs_from = ["generator"]
        )

        responce = results["generator"]["replies"][0].text
        st.markdown("### 📌 Answer")
        st.write(responce)
