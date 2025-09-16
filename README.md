# 📄 ResuMatch AI

**ResuMatch AI** is an AI-powered tool that helps candidates generate **ATS-friendly resumes** and **personalized cold emails** by analyzing job descriptions and portfolio links.  
Built with **LangChain**, **Groq LLMs**, and **Python-docx**, it automates the tedious process of resume tailoring and recruiter outreach.

---

## ✨ Features

✅ **Job Description Parsing** – Extracts role, skills, and requirements from raw job descriptions  
✅ **Cold Email Generation** – Writes recruiter-ready professional emails  
✅ **ATS-Friendly Resume Builder** – Generates a compact, one-page resume in Word format  
✅ **Smart Project Handling** – Deduplicates portfolio links and limits to 2–3 projects per resume  
✅ **Minimal Spacing Design** – Clean look with thin blue dividers (no extra white space)  
✅ **Customizable Sections** – Summary → Education → Skills → Projects → Achievements  

---

## 🛠 Tech Stack

- 🐍 **Backend** → Python  
- 🔗 **Framework** → LangChain  
- ⚡ **LLM** → Groq (Llama 3.3 70B Versatile)  
- 📄 **Document Generation** → python-docx  
- 🔑 **Secrets Management** → python-dotenv  

---

## 📂 Project Structure

ResuMatch-AI/
│── chains.py # Core logic for JD parsing, email writing, and resume generation
│── requirements.txt # Dependencies
│── .env.example # Environment variable template (Groq API key)
│── README.md # Project documentation

--

## ⚙️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/ResuMatch-AI.git
   cd ResuMatch-AI

```

2. **Create a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate   # On Linux/Mac
.venv\Scripts\activate      # On Windows
```
3.**Install dependencies**
```bash
pip install -r requirements.txt
```
4. **Set up environment variables**
 ```bash
 .env.example → .env
```

5.** Add your Groq API key:**
  ```bash
GROQ_API_KEY=your_api_key_here
```
6. **Run the script**
```bash
python chains.py
```
🚀 Usage
---
**Extract job details**

   ```bash
chain = Chain()
job_info = chain.extract_jobs(jd_text="Job description here...")
```
**Generate cold email**

   ```bash
email = chain.write_mail(job_info, links, "Your Name", "Your Background", "youremail@example.com")
print(email)
```
**Create resume**

   ```bash
resume_file = chain.write_resume(job_info, "Your Name", "Your Background", "youremail@example.com", links)
print("Resume saved at:", resume_file)
```
---


** Sample Output**
---
Generated Resume (Word format)

Compact, font size 10

Minimal spacing with thin blue dividers

Projects limited to 2–3 with concise bullet points

ATS-friendly formatting


---


**🏆 Achievements**


---
Automated resume tailoring for multiple job applications

Improved candidate–recruiter outreach with AI-written cold emails

Ensures ATS-compatibility by keeping resumes clean and structured
---


🤝 **Contributing**
---
Contributions are welcome! Feel free to fork this repo, open an issue, or submit a pull request.

📧 Contact
👤 Kavisha Gupta
📩 Email: kavishagupta8806@gmail.com
🔗 LinkedIn | GitHub


---


