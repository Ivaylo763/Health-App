import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# Cache the OCR model (IMPORTANT 🚀)
@st.cache_resource
def load_reader():
    return easyocr.Reader(['bg', 'en'])

reader = load_reader()

# List of harmful ingredients
HARMFUL_LIST = [
    "E102", "E110", "E120", "E124", "E127",
    "E129", "E133", "E150", "E211", "E250",
    "E621", "E951", "ASPARTAME", "MSG", "КОНСЕРВАНТИ"
]

def normalize_text(text):
    # Normalize text to catch variations like "e 102", "e-102"
    text = text.upper()
    text = text.replace("-", "").replace(" ", "")
    return text

def process_image(image):
    img_array = np.array(image)
    results = reader.readtext(img_array, detail=0)
    return " ".join(results)

# --- Streamlit UI ---
st.set_page_config(page_title="Е-Скенер", page_icon="🚫")
st.title("🧪 Проверка за вредни Е-номера")

uploaded_file = st.file_uploader("Качете снимка на етикет", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    # FIXED (new Streamlit style)
    st.image(image, caption='Качено изображение', width="stretch")

    with st.spinner('Сканиране на съставките...'):
        try:
            extracted_text = process_image(image)
            normalized_text = normalize_text(extracted_text)

            st.subheader("Разпознати съставки:")
            st.write(extracted_text)

            found_ingredients = []
            for item in HARMFUL_LIST:
                if normalize_text(item) in normalized_text:
                    found_ingredients.append(item)

            st.divider()

            if found_ingredients:
                st.error(
                    f"⚠️ ВНИМАНИЕ! Открити вредни съставки: {', '.join(found_ingredients)}"
                )
                st.info("Препоръчително е да избягвате продукти с тези добавки.")
            else:
                st.success("✅ Не бяха открити съставки от списъка с вредни вещества.")

        except Exception as e:
            st.error(f"Грешка при обработката: {e}")
