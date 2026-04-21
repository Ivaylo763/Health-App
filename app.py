import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# 1. Списък с вредни съставки (можеш лесно да добавяш нови тук)
HARMFUL_LIST = [
    "E102", "E110", "E120", "E124", "E127", 
    "E129", "E133", "E150", "E211", "E250", 
    "E621", "E951", "ASPARTAME", "MSG", "КОНСЕРВАНТИ"
]

def process_image(image):
    # Инициализиране на EasyOCR
    reader = easyocr.Reader(['bg', 'en'])
    img_array = np.array(image)
    # Извличаме само текста и го обединяваме в един низ
    results = reader.readtext(img_array, detail=0)
    return " ".join(results).upper()

# --- Streamlit Интерфейс ---
st.set_page_config(page_title="Е-Скенер", page_icon="🚫")
st.title("🧪 Проверка за вредни Е-номера")

uploaded_file = st.file_uploader("Качете снимка на етикет", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Качено изображение', use_container_width=True)
    
    with st.spinner('Сканиране на съставките...'):
        try:
            # Извличане на текста от снимката
            extracted_text = process_image(image)
            
            st.subheader("Разпознати съставки:")
            st.write(extracted_text)
            
            # Проверка чрез списъка
            found_ingredients = []
            for item in HARMFUL_LIST:
                if item in extracted_text:
                    found_ingredients.append(item)
            
            st.divider()
            
            # Показване на резултата
            if found_ingredients:
                st.error(f"⚠️ ВНИМАНИЕ! Открити вредни съставки: {', '.join(found_ingredients)}")
                st.info("Препоръчително е да избягвате продукти с тези добавки.")
            else:
                st.success("✅ Не бяха открити съставки от списъка с вредни вещества.")
                
        except Exception as e:
            st.error(f"Грешка при обработката: {e}")
