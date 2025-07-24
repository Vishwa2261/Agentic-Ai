import streamlit as st
import pdfplumber
import google.generativeai as genai

# --- Configure Gemini API ---
genai.configure(api_key="AIzaSyDivRsmlLOqEtTJe9kEMXC9w6RiKqnYWsc")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Streamlit UI Setup ---
st.set_page_config(page_title="📄 Resume Reviewer AI", layout="centered")
st.title("🧠 Professional Resume Reviewer")
st.markdown("Upload your resume (PDF or TXT). Get structured, AI-generated feedback to make it job-market ready.")

# --- File Upload ---
resume_file = st.file_uploader("📎 Upload your resume (PDF or TXT)", type=["pdf", "txt"])

def extract_text(file):
    if file.type == "application/pdf":
        with pdfplumber.open(file) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    else:
        return ""

# --- Main Logic ---
if resume_file:
    resume_text = extract_text(resume_file)
    
    if not resume_text.strip():
        st.error("Could not extract text from the file.")
    else:
        st.subheader("📝 Resume Content Preview")
        with st.expander("Click to preview raw text"):
            st.text_area("Extracted Resume Text", resume_text, height=300)

        # Construct prompt for Gemini
        prompt = f"""
You are a professional resume reviewer. Analyze the following resume content and provide structured feedback in Markdown format. 
Divide the feedback into these sections:

- **Summary**: General first impressions of the resume.
- **Skills**: Evaluate the technical and soft skills listed.
- **Work Experience**: Comment on clarity, impact, and use of action verbs in bullet points.
- **Projects**: Evaluate relevance, clarity, and technical depth of described projects.
- **Suggestions**: Detailed improvements regarding formatting, grammar, alignment to job roles, and overall professionalism.

Resume Content:
{resume_text}

Provide the feedback in well-formatted Markdown suitable for rendering in a Streamlit app.
"""

        if st.button("🔍 Analyze Resume"):
            with st.spinner("Analyzing with Gemini..."):
                response = model.generate_content(prompt)
                st.markdown("## 🧾 Resume Review")
                st.markdown(response.text)

else:
    st.info("Please upload a resume to begin analysis.")
