import uuid
import requests
import pandas as pd
import chromadb
from typing import List, Dict


class Portfolio:
    def __init__(self, data=None, file_path=None):
        # Persist Chroma index in ./vectorstore
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

        if file_path:
            self.data = pd.read_csv(file_path)
        elif data:
            self.data = pd.DataFrame(data)
        else:
            self.data = pd.DataFrame(columns=["Title", "Techstack", "Links"])

        # Normalize columns
        for col in ["Title", "Techstack", "Links"]:
            if col not in self.data.columns:
                self.data[col] = ""

        self.data["Title"] = self.data["Title"].astype(str).fillna("")
        self.data["Techstack"] = self.data["Techstack"].astype(str).fillna("")
        self.data["Links"] = self.data["Links"].astype(str).fillna("")

    @classmethod
    def from_github(cls, username: str):
        """Fetch public repos from GitHub as portfolio items."""
        url = f"https://api.github.com/users/{username}/repos?per_page=100"
        projects = []
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                for repo in r.json():
                    projects.append({
                        "Title": repo.get("name") or "Untitled Project",
                        "Techstack": repo.get("language") or "Unknown",
                        "Links": repo.get("html_url", "")
                    })
        except Exception:
            pass
        return cls(data=projects)

    @classmethod
    def from_form(cls, user_projects: List[Dict]):
        """Create portfolio from Streamlit form input."""
        rows = []
        for p in user_projects:
            rows.append({
                "Title": p.get("Title") or p.get("Project Title") or "Untitled Project",
                "Techstack": p.get("Techstack", ""),
                "Links": p.get("Links", "")
            })
        return cls(data=rows)

    def load_portfolio(self):
        """Index projects in Chroma (id stable by URL to avoid dupes)."""
        if self.collection.count() == 0 and not self.data.empty:
            docs, metas, ids = [], [], []
            for _, row in self.data.iterrows():
                link = row["Links"]
                if not link:
                    continue
                docs.append(row["Techstack"] or "project")
                metas.append({"links": link, "title": row.get("Title", "")})
                ids.append(f"pid_{uuid.uuid5(uuid.NAMESPACE_URL, link)}")
            if docs:
                self.collection.add(documents=docs, metadatas=metas, ids=ids)

    def query_links(self, skills):
        """
        Return a FLAT list of dicts like:
        [{'name': 'RepoName', 'link': 'https://github.com/...'}, ...]
        """
        if self.collection.count() == 0:
            return []

        # Accept str or list for skills
        if isinstance(skills, str):
            query_texts = [skills] if skills.strip() else ["software engineering"]
        else:
            safe_skills = [s for s in skills if isinstance(s, str) and s.strip()]
            query_texts = ["; ".join(safe_skills[:10])] + safe_skills[:3] if safe_skills else ["software engineering"]

        # Return a few best hits
        n_results = min(max(2, len(self.data)), 6) if not self.data.empty else 3
        out = self.collection.query(query_texts=query_texts, n_results=n_results)

        metas = out.get("metadatas", [])
        flat, seen = [], set()
        for group in metas:
            for m in group:
                link = (m or {}).get("links")
                title = (m or {}).get("title") or (link.split("/")[-1] if link else "Project")
                if link and link not in seen:
                    seen.add(link)
                    flat.append({"name": title, "link": link})
        return flat

    def top_n_fallback(self, n=3):
        """If vector query returns nothing, just take top-N from DataFrame."""
        flat, seen = [], set()
        for _, row in self.data.head(n).iterrows():
            link = row["Links"]
            if link and link not in seen:
                seen.add(link)
                title = row.get("Title") or (link.split("/")[-1] if link else "Project")
                flat.append({"name": title, "link": link})
        return flat
