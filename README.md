# 🌌 TARS Terminal

**TARS-Terminal-Your-AI-co-pilot-for-understand-Interstellar**

**TARS Terminal** is a sleek Retrieval-Augmented Generation (RAG) system tailored for answering questions from a specific knowledge base. This system was built using **Mistral**, **Haystack** and the UI by **Streamlit**. This project showcase the full RAG pipeline in action, using the movie _interstellar_ as a case study.

# 🚀 Features

* 🔍 Semantic search using In memory document store.

* 🧠 Contextual answer generation with the Mistral LLM

* 📚 Custom document ingestion and indexing

* 🌐 Intuitive Streamlit-based user interface

* 🧩 Modular architecture for easy customization


# 🧰 Technologies Used

* **Mistral**: Open-weight LLM for text generation (https://mistral.ai/)

* **Haystack**: Backend pipeline for RAG (https://haystack.deepset.ai/overview/intro)

* **Streamlit**: UI for rapid web app deployment (https://streamlit.io/)


# 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/tars-terminal.git
cd tars-terminal
```

2. (Recommended) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install haystack
pip install mistral-haystack
pip install streamlit
```

4. Get the API key from Mistralai. (https://console.mistral.ai/api-keys)

5. Add the prepared document URLs to the source code. (Note: Be carefull about the sources, the information should be structured and less noisy)

6. Run the app:

```bash
streamlit run interstellar.py
```

# 🧠 System Architecture

![System Architecture](Architecture.jpg)


# 🧪 Sample Use Case: Interstellar Knowledge Base

This project uses knowledge from Interstellar's plot, characters, science, and themes. Users can ask:

"What is the fifth dimension in Interstellar?"

"Explain the time dilation near the black hole."

"Who is TARS and what is his function?"

The system retrieves relevant information from indexed documents and provides contextual answers.


# 🔧 Customization Guide

Want to adapt the RAG system to your own domain?

1. Replace the URLs with your domain-specific documents.

2. (Optional) Fine tune the parameters like chunk size 

3. Modify the Streamlit UI (e.g., background image, text prompts).


# 📞 Contact

Created by [Kavindu Mihiran] - Feel free to reach out via GitHub or email!











