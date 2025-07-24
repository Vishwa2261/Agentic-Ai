import streamlit as st
import cv2
import numpy as np
from PIL import Image
import google.generativeai as genai
import io

# Configure Gemini
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit UI
st.set_page_config(page_title="🖼️ AI Photo Editor", layout="centered")
st.title("🎨 AI-Based Photo Editor")
st.markdown("Upload an image or use the camera. Apply filters like **Grayscale**, **Sepia**, **Blur**, or **Cartoon Effect**.")

# Image input
img_file = st.file_uploader("📁 Upload an Image", type=["jpg", "jpeg", "png"])
img_cam = st.camera_input("📷 Or take a photo")

# Priority: Camera over Upload
source_image = img_cam if img_cam else img_file

# Filter selection
filter_option = st.selectbox("🎛️ Choose a filter", ["None", "Grayscale", "Sepia", "Blur", "Cartoon Effect"])

def apply_filter(image, filter_type):
    img = np.array(image.convert("RGB"))
    if filter_type == "Grayscale":
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        return Image.fromarray(cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB))
    elif filter_type == "Sepia":
        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])
        sepia = cv2.transform(img, sepia_filter)
        sepia = np.clip(sepia, 0, 255)
        return Image.fromarray(sepia.astype(np.uint8))
    elif filter_type == "Blur":
        blurred = cv2.GaussianBlur(img, (15, 15), 0)
        return Image.fromarray(blurred)
    elif filter_type == "Cartoon Effect":
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(img, 9, 300, 300)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        return Image.fromarray(cartoon)
    else:
        return image

if source_image:
    # Load image using PIL
    image = Image.open(source_image)

    # Display original
    st.subheader("🖼️ Original Image")
    st.image(image, use_column_width=True)

    # Apply filter
    if filter_option != "None":
        filtered_img = apply_filter(image, filter_option)

        st.subheader(f"✨ Filter Applied: {filter_option}")
        st.image(filtered_img, use_column_width=True)

        # Optional Gemini explanation
        if st.checkbox("🤖 Explain this effect with Gemini"):
            prompt = f"Explain in simple terms what the '{filter_option}' filter does to an image."
            with st.spinner("Getting explanation..."):
                response = model.generate_content(prompt)
                st.markdown(f"**Gemini AI Explanation:**\n\n{response.text}")
    else:
        st.info("Select a filter to apply.")
else:
    st.info("Please upload an image or use your camera.")


