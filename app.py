import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# 1. Списък с вредни съставки
HARMFUL_LIST = [
    "E102", "E110", "E120", "E121", "E122", "E123", "E124", "E127", 
    "E129", "E131", "E132", "E133", "E142", "E150", "E151", "E153",
    "E154", "E155", "E173", "E174", "E175", "E180", "E211", "E250", 
    "E621", "E951", "ASPARTAME", "MSG"
]

# Функция за разпознаване на текст (кешираме я, за да не зарежда модела всеки път)
@st.cache_resource
def load_reader():
    return easyocr.Reader(['bg', 'en'])

def process_image(image):
    reader = load_reader()
    img_array = np.array(image)
    results = reader.readtext(img_array, detail=0)
    return " ".join(results).upper()

# --- Streamlit Интерфейс ---
st.set_page_config(page_title="Е-Скенер", page_icon="📸")
st.title("📸 Скенер за вредни съставки")

# Избор на метод за вход
option = st.radio("Изберете метод:", ("Снимка от камерата", "Качване на файл"))

image_file = None

if option == "Снимка от камерата":
    image_file = st.camera_input("Направете снимка на етикета")
else:
    image_file = st.file_uploader("Изберете снимка от устройството", type=["jpg", "jpeg", "png"])

if image_file is not None:
    image = Image.open(image_file)
    
    # Показваме снимката (само ако е качен файл, камерата сама показва преглед)
    if option == "Качване на файл":
        st.image(image, caption='Качено изображение', use_container_width=True)
    
    with st.spinner('Анализиране на съставките...'):
        try:
            extracted_text = process_image(image)
            
            st.subheader("Разпознат текст:")
            st.info(extracted_text)
            
            # Търсене в списъка
            found_ingredients = [item for item in HARMFUL_LIST if item in extracted_text]
            
            st.divider()
            
            if found_ingredients:
                st.error(f"⚠️ ВНИМАНИЕ! Открити вредни съставки: **{', '.join(found_ingredients)}**")
            else:
                st.success("✅ Не бяха открити съставки от черния списък.")
                
        except Exception as e:
            st.error(f"Грешка при обработката: {e}")
