import streamlit as st
import google.generativeai as genai

# Directly set the API key (WARNING: don't do this in production!)
genai.configure(api_key="AIzaSyDivRsmlLOqEtTJe9kEMXC9w6RiKqnYWsc")

# Initialize Gemini Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit UI Setup
st.set_page_config(page_title="AI Movie Recommender", layout="centered")
st.title("🎥 AI Movie Recommender with Gemini 2.0 Flash")
st.markdown("Get 10+ latest movie recommendations based on your preferences.")

# User Input
genre = st.text_input("Preferred Genre (e.g. Action, Drama):")
actor = st.text_input("Favorite Actor or Actress (optional):")
taste = st.text_input("Describe Your Movie Taste (e.g. emotional, thrilling):")

# On Button Click
if st.button("Recommend Movies"):
    if not genre:
        st.warning("Please enter at least a genre.")
    else:
        # Prompt for Gemini
        prompt = f"""
You are a movie expert. Recommend at least 10 of the latest movies (from the past 2–3 years).
Base your recommendations on:
- Genre: {genre}
- Actor/Actress: {actor if actor else 'Not specified'}
- Movie Taste: {taste if taste else 'Not specified'}

For each movie, include:
1. **Title**
2. **1–2 sentence description**

Format the output in markdown.
"""

        with st.spinner("Fetching movie recommendations from Gemini..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error fetching recommendations: {e}")

