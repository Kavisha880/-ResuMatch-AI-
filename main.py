import streamlit as st
from chain import Chain
from portfolio import Portfolio

st.set_page_config(page_title="ResuMatch AI", layout="wide")

st.title("📧 ResuMatch AI – Smart Cold Email & Resume Generator")

# --- User Info ---
st.subheader("👤 Your Info")
user_name = st.text_input("Full Name")
user_background = st.text_area("Background (short intro)")
user_email = st.text_input("Email")

# --- Job Info ---
st.subheader("📄 Job Description")
jd_text = st.text_area("Paste Job Description Here")

# --- Portfolio ---
st.subheader("📂 Portfolio Source")
github_username = st.text_input("GitHub Username (optional)")

if "projects" not in st.session_state:
    st.session_state["projects"] = []

projects = st.session_state["projects"]

if not github_username:
    st.write("Or manually add your projects")
    with st.form("project_form", clear_on_submit=True):
        title = st.text_input("Project Title")
        link = st.text_input("Project Link")
        techstack = st.text_input("Tech Stack (comma separated)")
        add_btn = st.form_submit_button("Add Project")
        if add_btn and link and techstack:
            projects.append({"Title": title or "Untitled Project", "Techstack": techstack, "Links": link})
    if projects:
        st.write(projects)

# --- Buttons ---
col1, col2 = st.columns(2)
with col1:
    email_btn = st.button("Generate Cold Email")
with col2:
    resume_btn = st.button("Generate Resume")

# --- Logic ---
if email_btn or resume_btn:
    chain = Chain()

    if github_username:
        portfolio = Portfolio.from_github(github_username)
    else:
        portfolio = Portfolio.from_form(projects)

    portfolio.load_portfolio()
    job_info = chain.extract_jobs(jd_text)[0]

    # Skills may come as list or a single string
    skills = job_info.get("skills", [])
    if isinstance(skills, str):
        # attempt to split if a single string
        skills = [s.strip() for s in skills.replace("|", ",").split(",") if s.strip()]

    links_flat = portfolio.query_links(skills)

    # FALLBACK if vector search returns nothing
    if not links_flat:
        links_flat = portfolio.top_n_fallback(n=3)

    # Uncomment for debugging:
    # st.write({"skills": skills, "links_flat": links_flat})

    if email_btn:
        email = chain.write_mail(job_info, links_flat, user_name, user_background, user_email)
        st.subheader("📧 Cold Email")
        st.code(email, language="markdown")

    if resume_btn:
        resume_file = chain.write_resume(job_info, user_name, user_background, user_email, links_flat)
        st.subheader("📄 Resume Generated")
        with open(resume_file, "rb") as f:
            st.download_button("Download Resume", f, file_name=resume_file)
