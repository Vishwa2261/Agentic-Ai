import streamlit as st
import google.generativeai as genai

# --- Configure Gemini API ---
genai.configure(api_key="AIzaSyDivRsmlLOqEtTJe9kEMXC9w6RiKqnYWsc")

# --- Load the Gemini Flash Model ---
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Streamlit UI ---
st.set_page_config(page_title="🧮 Math Problem Solver AI", layout="centered")
st.title("🧠 Math Problem Solver AI")
st.markdown("Enter any mathematical expression or equation below and get a detailed, beginner-friendly explanation.")

# --- User Input ---
user_input = st.text_area("✍️ Type your math problem here (e.g., `2x + 3 = 9`, `integrate(x^2)`, `limit(x->0) sin(x)/x`)", height=100)

if st.button("🧮 Solve"):
    if user_input.strip() == "":
        st.warning("Please enter a valid math problem.")
    else:
        # Prompt for Gemini
        prompt = f"""
You are a Math Problem Solver AI. When a user inputs a mathematical expression or equation (like: `{user_input}`),
you will provide a clear, step-by-step solution. Make it beginner-friendly and use markdown formatting for better rendering.

Problem:
{user_input}

Provide solution below:
"""

        with st.spinner("Solving..."):
            response = model.generate_content(prompt)
            st.markdown("### 📘 Step-by-Step Solution:")
            st.markdown(response.text)

