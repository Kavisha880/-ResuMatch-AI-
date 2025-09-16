from chain import Chain
from portfolio import Portfolio

# 1. Sample Job Description
jd_text = """
We are looking for an AI Engineer with 0–2 years of experience.
The ideal candidate should have strong skills in Python, NLP, and Large Language Models (LLMs).
Hands-on experience with LangChain, Vector Databases (like ChromaDB or FAISS), and Streamlit is preferred.
Exposure to building recommendation systems or computer vision projects is a plus.
"""

# 2. Initialize Chain and Portfolio (use CSV for now)
chain = Chain()
portfolio = Portfolio(file_path="resource/my_portfolio.csv")
portfolio.load_portfolio()

# 3. Extract structured job info
job_info = chain.extract_jobs(jd_text)[0]
print("Extracted Job Info:\n", job_info)

# 4. Query portfolio for matching projects
skills = job_info.get("skills", [])
links = portfolio.query_links(skills)
print("\nMatching Projects:\n", links)

# 5. Generate Cold Email (user fills this info)
user_name = "Rahul Sharma"
user_background = "Final year B.Tech student specializing in AI/ML"
user_email = "rahul.sharma@example.com"

email = chain.write_mail(job_info, links, user_name, user_background, user_email)
print("\nGenerated Cold Email:\n", email)
