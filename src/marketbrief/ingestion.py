from dataclasses import dataclass
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

@dataclass
class Article:
    url: str
    title: str
    text: str

def validate_url(url: str) -> bool:
    try:
        p=urlparse(url.strip())
        return p.scheme in {"http","https"} and bool(p.netloc)
    except ValueError:
        return False

def extract_article(html: str, url: str="") -> Article:
    soup=BeautifulSoup(html,"html.parser")
    for n in soup(["script","style","noscript","svg","nav","footer","header","form","aside"]):
        n.decompose()
    title=soup.title.get_text(" ",strip=True) if soup.title else ""
    if not title:
        h=soup.find(["h1","h2"])
        title=h.get_text(" ",strip=True) if h else url
    main=soup.find("article") or soup.find("main") or soup.body or soup
    parts=[p.get_text(" ",strip=True) for p in main.find_all(["p","h1","h2","h3","li"])]
    text="\\n".join(x for x in parts if len(x)>35)
    if not text: text=main.get_text(" ",strip=True)
    return Article(url,title[:300],text.strip())

def fetch_article(url: str, timeout: int=15) -> Article:
    if not validate_url(url): raise ValueError("Only valid http:// or https:// URLs are accepted.")
    r=requests.get(url,headers={"User-Agent":"MarketBriefResearchAssistant/1.0"},timeout=timeout)
    r.raise_for_status()
    c=r.headers.get("content-type","").lower()
    if "text/html" not in c: raise ValueError(f"Unsupported content type: {c or 'unknown'}")
    a=extract_article(r.text,url)
    if len(a.text)<200: raise ValueError("Could not extract enough readable article text.")
    return a
