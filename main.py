import streamlit as st
from portfolio import Portfolio
from chain import Chain

st.set_page_config(page_title="ResuMatch AI", page_icon="📧", layout="centered")
st.title("📧 ResuMatch AI – Smart Cold Email & Resume Generator")

# ---------------------------
# Session state for projects
# ---------------------------
if "projects" not in st.session_state:
    st.session_state["projects"] = []

projects = st.session_state["projects"]

# ---------------------------
# User Inputs
# ---------------------------
st.subheader("Your Info")
col_a, col_b = st.columns(2)
with col_a:
    user_name = st.text_input("Full Name", value="")
with col_b:
    user_email = st.text_input("Email", value="")

user_background = st.text_area("Background (short intro)", value="", placeholder="e.g., Final-year CSE (AI) student with hands-on GenAI & NLP projects.")

st.subheader("Job Description")
jd_text = st.text_area(
    "Paste the Job Description",
    height=220,
    placeholder="Paste the JD here (role, responsibilities, required skills, etc.)"
)

st.subheader("Portfolio Sources")
github_username = st.text_input("GitHub Username (optional)", value="")

st.caption("Or add 2–5 of your best projects manually:")
with st.form("project_form", clear_on_submit=True):
    title = st.text_input("Project Title")
    link = st.text_input("Project Link")
    techstack = st.text_input("Tech Stack (comma separated)")
    add_btn = st.form_submit_button("Add Project")

    # ✅ Validate link so junk doesn't enter the index
    if add_btn and link and techstack:
        if not (link.startswith("http://") or link.startswith("https://")):
            st.warning("Please enter a valid URL (must start with http:// or https://).")
        else:
            projects.append({
                "Title": title or "Untitled Project",
                "Techstack": techstack,
                "Links": link
            })
            st.success("Project added.")

# Show current manual projects
if projects:
    st.write("**Manual Projects Added:**")
    for i, p in enumerate(projects, start=1):
        st.write(f"- {i}. **{p.get('Title','Untitled Project')}** — {p.get('Techstack','')}  \n  {p.get('Links','')}")

# ---------------------------
# Actions
# ---------------------------
st.subheader("Generate")
col1, col2 = st.columns(2)
with col1:
    email_btn = st.button("Generate Cold Email")
with col2:
    resume_btn = st.button("Generate Resume (.docx)")

# ✅ Require JD before proceeding
if (email_btn or resume_btn) and not jd_text.strip():
    st.error("Please paste a Job Description before generating.")
    st.stop()

# ---------------------------
# Build Portfolio (GitHub or Form)
# ---------------------------
portfolio = None
if github_username.strip():
    portfolio = Portfolio.from_github(github_username.strip())
    # Optional UX: if GitHub yielded nothing, hint user to use manual
    if getattr(portfolio, "data", None) is not None and portfolio.data.empty:
        st.info("Couldn’t fetch GitHub repos (rate limit or username issue). Add projects manually below.")
else:
    portfolio = Portfolio.from_form(projects)

# Load vector index (or fallback cache)
portfolio.load_portfolio()

# ---------------------------
# Generate (Email / Resume)
# ---------------------------
if email_btn or resume_btn:
    # Initialize LLM chain (reads GROQ key from env or st.secrets)
    chain = Chain()

    # ✅ Safe JD parsing (LLM → structured JSON)
    try:
        job_info = chain.extract_jobs(jd_text)[0]  # expect dict with role/experience/skills/description
    except Exception as e:
        st.error(f"Could not parse the Job Description. Try a simpler JD. Details: {e}")
        st.stop()

    # Query matching portfolio links using JD text as query terms
    links_flat = portfolio.query_links(jd_text)
    if not links_flat:  # final guard
        links_flat = portfolio.top_n_fallback(n=3)

    if email_btn:
        with st.spinner("Writing your cold email..."):
            email_text = chain.write_mail(
                job=job_info,
                links_flat=links_flat,
                user_name=user_name,
                user_background=user_background,
                user_email=user_email
            )
        st.success("Cold email ready. You can copy it below:")
        st.text_area("Email", value=email_text, height=300)

    if resume_btn:
        with st.spinner("Building your ATS-friendly resume..."):
            file_path = chain.write_resume(
                job=job_info,
                user_name=user_name,
                user_background=user_background,
                user_email=user_email,
                projects=links_flat
            )
        st.success("Resume ready.")
        # Offer download
        with open(file_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Resume (.docx)",
                data=f.read(),
                file_name=file_path,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

# Footer
st.caption("Tip: Provide a clean JD and 2–5 strong project links for best results.")
