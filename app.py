import streamlit as st
from PIL import Image
import numpy as np
import easyocr
import re

st.set_page_config(page_title="Food Scanner")

st.title("🧾 Food Ingredient Scanner")

@st.cache_resource
def load_reader():
    return easyocr.Reader(['bg', 'en'], gpu=False)

reader = load_reader()

harmful_ingredients = {
    "e621": "MSG",
    "msg": "MSG",
    "палмово масло": "Palm Oil",
    "palm oil": "Palm Oil",
    "аспартам": "Aspartame",
    "aspartame": "Aspartame",
    "e950": "Acesulfame K",
    "e951": "Aspartame",
    "e952": "Cyclamate",
    "e954": "Saccharin",
    "e955": "Sucralose",
    "e102": "Tartrazine",
    "e110": "Sunset Yellow",
    "e124": "Ponceau 4R",
    "e129": "Allura Red"
}

uploaded_file = st.file_uploader(
    "Upload food label image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(image, use_container_width=True)

    with st.spinner("Scanning..."):

        img = np.array(image)

        result = reader.readtext(img)

        text = " ".join([r[1] for r in result])

    st.subheader("Detected Text")

    st.text_area("", text, height=250)

    st.subheader("Potential Harmful Ingredients")

    found = []

    lower_text = text.lower()

    for ingredient, desc in harmful_ingredients.items():

        pattern = r'\b' + re.escape(ingredient) + r'\b'

        if re.search(pattern, lower_text):
            found.append((ingredient, desc))

    if found:

        for ingredient, desc in found:
            st.error(f"⚠️ {ingredient.upper()} → {desc}")

    else:
        st.success("No harmful ingredients detected.")
