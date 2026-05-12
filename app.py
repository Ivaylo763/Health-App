# app.py
# Приложение: Streamlit + EasyOCR за разпознаване на текст и откриване на вредни съставки
# Поддържа български и английски език

import streamlit as st
import easyocr
from PIL import Image
import numpy as np
from io import BytesIO

# 1) Дефиниране на вредни съставки за двата езика
HARMFUL_BG = [
    "e621", "е621",
    "палмово масло",
    "хидрогенизирани мазнини",
    "хидрогенирани мазнини",
    "моносодиум глутамат",
    "глутамат натрий",
    "глутамат"
]

HARMFUL_EN = [
    "e621", "monosodium glutamate", "msg",
    "palm oil", "palmoil",
    "hydrogenated", "partially hydrogenated",
    "trans fat",
    "sodium nitrite",
    "artificial flavors"
]

KEYWORDS = {
    "bg": HARMFUL_BG,
    "en": HARMFUL_EN
}


# 2) Кеширане на EasyOCR читател (за по-бързо стартиране)
@st.cache(allow_output_mutation=True)
def get_reader():
    # Поддържат се bg + en
    return easyocr.Reader(['bg','en'], gpu=False)

# 3) Преобразуване на текст за проверка
def detect_harmful(full_text, lang_key):
    lower = full_text.lower()
    keywords = KEYWORDS.get(lang_key, [])
    found = [k for k in keywords if k.lower() in lower]
    return list(dict.fromkeys(found))  # премахва дублиращи се

# 4) Основна функция на приложението
def main():
    st.set_page_config(page_title="OCR с проверка на вредни съставки", layout="wide")

    # Език на интерфейса
    lang_choice = st.sidebar.radio("Език / Language", ["Български", "English"])
    if lang_choice == "Български":
        lang_key = "bg"
        t = lambda bg, en: bg
        title = "OCR приложение: разпознаване на текст и проверка за вредни съставки"
        upload_label = "Качване на снимка"
        image_caption = "Каченото изображение"
        processed_label = "Извлечен текст"
        harmful_label = "Намерени вредни съставки"
        no_harmful = "Не са открити вредни съставки"
        results_label = "Резултати"
        help_text = "Съвет: Опитайте ясно, добре осветено изображение за по-добри резултати."
        start_button = "Разпознай текст"
    else:
        lang_key = "en"
        t = lambda bg, en: en
        title = "OCR App: Text extraction and harmful ingredients check"
        upload_label = "Upload an image"
        image_caption = "Uploaded image"
        processed_label = "Extracted text"
        harmful_label = "Detected harmful ingredients"
        no_harmful = "No harmful ingredients found"
        results_label = "Results"
        help_text = "Tip: Provide clear, well-lit images for better results."
        start_button = "Recognize text"

    st.title(title)

    # 5) Файл за качване
    uploaded_file = st.file_uploader(upload_label, type=["png","jpg","jpeg","bmp","gif"])

    # 6) Инициализиране на reader
    reader = get_reader()

    if uploaded_file is not None:
        # Четене на изображението
        image = Image.open(BytesIO(uploaded_file.getvalue())).convert('RGB')
        image_np = np.array(image)

        st.image(image, caption=image_caption, use_column_width=True)

        with st.spinner("Извличане на текст..."):
            texts = reader.readtext(image_np, detail=0)  # връща списък с текстови елементи
            full_text = " ".join(texts)
            full_text_lc = full_text.lower()

        # Показване на резултата
        st.subheader(processed_label)
        st.write(full_text)

        # Намиране на вредни съставки
        harmful_found = detect_harmful(full_text_lc, lang_key)

        st.subheader(results_label)
        if harmful_found:
            st.write(harmful_label + ":")
            for item in harmful_found:
                st.write("- " + item)
        else:
            st.write(no_harmful)

        st.info(help_text)

if __name__ == "__main__":
    main()
