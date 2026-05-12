# app.py

import streamlit as st
from PIL import Image
import numpy as np
import easyocr
import re

# =========================
# Конфигурация
# =========================

st.set_page_config(
    page_title="Food Ingredient Scanner",
    layout="centered"
)

st.title("🧾 OCR Scanner за вредни съставки")
st.write(
    "Качи снимка на етикет с продукти. "
    "Приложението ще разпознае текста и ще открие потенциално вредни съставки."
)

# =========================
# EasyOCR Reader
# =========================

@st.cache_resource
def load_reader():
    return easyocr.Reader(['bg', 'en'])

reader = load_reader()

# =========================
# Списък с вредни съставки
# =========================

harmful_ingredients = {
    "e621": "Мононатриев глутамат (MSG)",
    "msg": "Мононатриев глутамат (MSG)",
    "палмово масло": "Палмово масло",
    "palm oil": "Palm Oil",
    "аспартам": "Aspartame",
    "aspartame": "Aspartame",
    "e950": "Ацесулфам K",
    "e951": "Aspartame",
    "e952": "Cyclamate",
    "e954": "Saccharin",
    "e955": "Sucralose",
    "e211": "Sodium Benzoate",
    "натриев бензоат": "Sodium Benzoate",
    "e102": "Tartrazine",
    "e110": "Sunset Yellow",
    "e124": "Ponceau 4R",
    "e129": "Allura Red",
    "хидрогенирани мазнини": "Hydrogenated fats",
    "hydrogenated": "Hydrogenated fats",
}

# =========================
# Upload
# =========================

uploaded_file = st.file_uploader(
    "Качи снимка",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(image, caption="Качена снимка", use_container_width=True)

    # =========================
    # OCR
    # =========================

    with st.spinner("Разпознаване на текст..."):

        img_array = np.array(image)

        results = reader.readtext(img_array)

        extracted_text = " ".join([res[1] for res in results])

    st.subheader("📄 Разпознат текст")

    st.text_area(
        "OCR резултат",
        extracted_text,
        height=250
    )

    # =========================
    # Търсене на съставки
    # =========================

    st.subheader("⚠️ Намерени потенциално вредни съставки")

    found = []

    text_lower = extracted_text.lower()

    for ingredient, description in harmful_ingredients.items():

        pattern = r'\b' + re.escape(ingredient.lower()) + r'\b'

        if re.search(pattern, text_lower):
            found.append((ingredient, description))

    if found:

        for ingredient, description in found:
            st.error(f"{ingredient.upper()} → {description}")

    else:
        st.success("Не са открити вредни съставки.")

# =========================
# Footer
# =========================

st.markdown("---")
st.caption("EasyOCR + Streamlit + Python")
