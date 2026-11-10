# MarketBrief AI — News Research Assistant

An independent news-research workspace inspired by the Codebasics news-analysis project. Add public article URLs, extract readable text, create a FAISS semantic index, and ask questions with source references.

## Features
- Multi-URL article ingestion with fetch diagnostics and timeouts
- HTML cleanup with BeautifulSoup
- LangChain document chunking and metadata preservation
- OpenAI embeddings + FAISS vector search
- Grounded Q&A using retrieved article excerpts
- Streamlit UI and source URL display
- Tests for URL validation, extraction, and chunk metadata

## Setup (Windows CMD)
Python 3.10+ recommended.

```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```
Add `OPENAI_API_KEY=your_api_key_here` to `.env`, then run:
```cmd
streamlit run app.py
```

## Workflow
1. Paste publicly accessible article URLs, one per line.
2. Build the research index.
3. Review successfully indexed sources.
4. Ask questions and inspect cited source URLs.

## Example questions
- What key risks are mentioned across these articles?
- Compare the outlook described by the different sources.
- Which claims are supported by more than one article?
- What evidence is missing?

## Architecture
```text
URLs -> Fetch + HTML cleanup -> LangChain Documents -> Chunking
     -> OpenAI Embeddings -> FAISS -> Similarity Retrieval
     -> Grounded Chat Model -> Answer + Source URLs
```

## Stack
Streamlit, Requests, BeautifulSoup, LangChain, OpenAI, FAISS.

## Limitations
This is an independent implementation, not a copy of the reference. Extraction is best-effort; some publishers block automated access, require JavaScript, or use paywalls. The app does not bypass restrictions. The FAISS index is held in Streamlit session memory and is cleared on restart. Answers can be incomplete or wrong; verify important claims against original sources. No live market data, financial advice, authentication, multi-user isolation, or cloud deployment is included. OpenAI API usage may incur charges.

## Tests
```cmd
python -m unittest discover -s tests -v
```
Tests do not call external APIs.

MIT License.
