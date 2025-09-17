import pandas as pd
import chromadb
import uuid
import requests

class Portfolio:
    def __init__(self, data=None, file_path=None):
        # self.chroma_client = chromadb.PersistentClient('vectorstore')
        
        client = chromadb.Client()

        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

        if file_path:   # Load from CSV
            self.data = pd.read_csv(file_path)
        elif data:      # Load from dict/list (form or GitHub)
            self.data = pd.DataFrame(data)
        else:
            self.data = pd.DataFrame()

    @classmethod
    def from_github(cls, username):
        """Fetch repos from GitHub API and load as portfolio"""
        url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(url)
        projects = []
        if response.status_code == 200:
            for repo in response.json():
                projects.append({
                    "Techstack": repo.get("language", "Unknown"),
                    "Links": repo["html_url"]
                })
        return cls(data=projects)

    @classmethod
    def from_form(cls, user_projects):
        """Load portfolio from Streamlit form input"""
        return cls(data=user_projects)

    def load_portfolio(self):
        if not self.collection.count() and not self.data.empty:
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=row["Techstack"],
                    metadatas={"links": row["Links"]},
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        if self.collection.count() == 0:
            return []
        return self.collection.query(query_texts=skills, n_results=2).get("metadatas", [])
