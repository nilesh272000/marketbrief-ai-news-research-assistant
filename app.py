import os
import streamlit as st
from dotenv import load_dotenv
from src.marketbrief.ingestion import fetch_article
from src.marketbrief.indexing import articles_to_chunks,build_faiss_index
from src.marketbrief.qa import answer_question

load_dotenv()
st.set_page_config(page_title="MarketBrief AI",page_icon="📰",layout="wide")
st.title("📰 MarketBrief AI")
st.caption("News research assistant | Collect articles, build a semantic index, and ask source-grounded questions.")
with st.sidebar:
    st.header("Research setup")
    key=st.text_input("OpenAI API key",value=os.getenv("OPENAI_API_KEY",""),type="password")
    chat=os.getenv("OPENAI_CHAT_MODEL","gpt-4o-mini")
    embed=os.getenv("OPENAI_EMBEDDING_MODEL","text-embedding-3-small")
    st.caption("API usage may incur charges. Avoid confidential content.")
if "vs" not in st.session_state: st.session_state.vs=None
if "articles" not in st.session_state: st.session_state.articles=[]
if "history" not in st.session_state: st.session_state.history=[]
st.subheader("1. Add news articles")
raw=st.text_area("Paste public article URLs (one per line)",height=130)
if st.button("Build research index",type="primary",disabled=not raw.strip()):
    urls=list(dict.fromkeys(x.strip() for x in raw.splitlines() if x.strip()))
    articles=[]; bar=st.progress(0)
    for i,url in enumerate(urls):
        try:
            a=fetch_article(url); articles.append(a); st.write("✓ Extracted:",a.title)
        except Exception as e: st.warning(f"{url}: {e}")
        bar.progress((i+1)/len(urls))
    if articles:
        try:
            chunks=articles_to_chunks(articles)
            with st.spinner(f"Embedding and indexing {len(chunks)} chunks..."):
                st.session_state.vs=build_faiss_index(chunks,key,embed)
            st.session_state.articles=articles
            st.success(f"Indexed {len(articles)} article(s), {len(chunks)} chunks.")
        except Exception as e: st.error(f"Indexing failed: {e}")
    else: st.error("No articles could be extracted.")
if st.session_state.articles:
    st.subheader("2. Indexed sources")
    for a in st.session_state.articles: st.markdown(f"- [{a.title or a.url}]({a.url})")
st.subheader("3. Ask a research question")
q=st.text_input("Question",placeholder="What key risks are mentioned across these articles?")
if st.button("Research answer",disabled=st.session_state.vs is None or not q.strip()):
    try:
        with st.spinner("Retrieving evidence and generating answer..."):
            ans,src=answer_question(st.session_state.vs,q,key,chat)
        st.session_state.history.append({"q":q,"a":ans,"s":src})
    except Exception as e: st.error(f"Could not answer: {e}")
for item in reversed(st.session_state.history):
    with st.container(border=True):
        st.markdown("**Question:** "+item["q"])
        st.markdown(item["a"])
        if item["s"]:
            st.markdown("**Sources**")
            for s in item["s"]: st.markdown(f"- [Source {s['id']}: {s['title']}]({s['url']})")
st.divider()
st.caption("Research aid only. Verify important claims against original publisher articles.")
