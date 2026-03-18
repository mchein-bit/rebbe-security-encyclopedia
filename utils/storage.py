import json
import os
import uuid
from datetime import datetime

ARTICLES_FILE = "articles.json"

CATEGORIES = [
    "Principles & Halacha",
    "Wars & Military Operations",
    "People",
    "Diplomacy & Peace Negotiations",
    "Territories & Geography",
    "Prophecy & Spiritual Dimensions",
    "Other",
]

def load_articles():
    if not os.path.exists(ARTICLES_FILE):
        return []
    try:
        with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_articles(articles):
    with open(ARTICLES_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

def add_article(article_data: dict):
    articles = load_articles()
    article_data["id"] = str(uuid.uuid4())
    article_data["created_at"] = datetime.now().isoformat()
    articles.append(article_data)
    save_articles(articles)
    return article_data["id"]

def get_article_by_id(article_id: str):
    for a in load_articles():
        if a.get("id") == article_id:
            return a
    return None

def get_articles_by_category(articles, category):
    return [a for a in articles if a.get("category") == category]

def search_articles(query: str):
    q = query.lower()
    results = []
    for a in load_articles():
        searchable = (a.get("title","") + " " + a.get("summary","") + " " + a.get("question","")).lower()
        if q in searchable:
            results.append(a)
    return results

def find_related_articles(article, all_articles, n=4):
    """Find related articles by category and keyword overlap."""
    cat = article.get("category","")
    aid = article.get("id","")
    title_words = set(article.get("title","").lower().split())
    
    scored = []
    for a in all_articles:
        if a.get("id") == aid:
            continue
        score = 0
        if a.get("category") == cat:
            score += 2
        other_words = set(a.get("title","").lower().split())
        overlap = len(title_words & other_words)
        score += overlap
        if score > 0:
            scored.append((score, a))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    return [a for _, a in scored[:n]]
