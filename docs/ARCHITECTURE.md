# Architecture

1. URL validation and bounded HTTP fetch.
2. BeautifulSoup removes common navigation, scripts, and boilerplate; article/main content is preferred.
3. Extracted content becomes LangChain Documents with title and source URL metadata.
4. RecursiveCharacterTextSplitter creates overlapping chunks.
5. OpenAI embeddings vectorize chunks; FAISS performs similarity search.
6. Retrieved passages are sent to a chat model with instructions to stay grounded and cite source labels.
7. Streamlit session state holds the index and Q&A history until the session ends.

The current design is intentionally small and inspectable. Production use requires persistence, isolation, observability, and a reviewed ingestion policy.
