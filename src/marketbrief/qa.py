from langchain_core.prompts import ChatPromptTemplate

SYSTEM="""You are MarketBrief, an assistant for research analysts. Answer only from supplied
article excerpts. If evidence is insufficient, say so. Distinguish reported facts from
interpretation. Never invent figures, dates, quotes, or causes. Cite evidence as [Source 1]."""

def answer_question(vectorstore,question,api_key,chat_model="gpt-4o-mini",k=5):
    if not question.strip(): raise ValueError("Please enter a research question.")
    if not api_key: raise ValueError("OPENAI_API_KEY is required.")
    docs=vectorstore.similarity_search(question,k=k)
    if not docs: return "No relevant article passages were retrieved.",[]
    ids={}; context=[]
    for d in docs:
        url=d.metadata.get("source","Unknown")
        if url not in ids: ids[url]=len(ids)+1
        context.append(f"[Source {ids[url]}] {d.metadata.get('title','Article')}\\nURL: {url}\\n{d.page_content}")
    prompt=ChatPromptTemplate.from_messages([("system",SYSTEM),
        ("human","Research question: {question}\\n\\nArticle excerpts:\\n{context}")])
    from langchain_openai import ChatOpenAI
    result=(prompt|ChatOpenAI(model=chat_model,temperature=0,api_key=api_key)).invoke(
        {"question":question,"context":"\\n\\n---\\n\\n".join(context)})
    sources=[]
    for url,i in ids.items():
        title=next((d.metadata.get("title","Article") for d in docs if d.metadata.get("source")==url),"Article")
        sources.append({"id":i,"title":title,"url":url})
    return result.content,sources
