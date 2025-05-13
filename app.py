import streamlit as st
import openai
from PIL import Image
import pytesseract
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY", "your-openai-api-key")

st.set_page_config(page_title="CommonLit AI Screenshot Helper", layout="centered")
st.title("📚 CommonLit AI Screenshot Helper")

st.markdown("Upload a screenshot of a CommonLit passage and question. The AI will extract the text and provide an answer.")

# Upload image
uploaded_file = st.file_uploader("Upload a screenshot (JPG or PNG):", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Screenshot", use_column_width=True)

    # OCR the image
    st.info("Extracting text from image...")
    extracted_text = pytesseract.image_to_string(image)

    st.subheader("Extracted Text")
    passage_text = st.text_area("Review and edit the extracted text below:", value=extracted_text, height=200)

    question = st.text_input("Enter your question about the passage:")

    if st.button("Get Answer"):
        if not passage_text or not question:
            st.warning("Please provide both the passage and a question.")
        else:
            with st.spinner("Thinking..."):
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a helpful reading tutor."},
                            {"role": "user", "content": f"Passage:\n{passage_text}\n\nQuestion: {question}"}
                        ],
                        max_tokens=500
                    )
                    answer = response.choices[0].message["content"].strip()
                    st.success("AI Answer:")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.warning("Please upload a screenshot to begin.")
