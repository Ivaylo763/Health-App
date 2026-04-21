

import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# 1. Речник с примери за вредни съставки (Е-номера)
# Можете да го разширите с реални данни
HARMFUL_INGREDIENTS = {
    "E102": "Тартразин (Оцветител) - Може да причини хиперактивност.",
    "Е110": "Сънсет Йелоу.",
    "Е120": "Кошенил.",
    "E129": "Алура червено (Оцветител) - Потенциален алерген.",
    "E211": "Натриев бензоат (Консервант) - Вреден при комбинация с Витамин С.",
    "Е220": "Серен диоксид",
    "Е250": "Натриев нитрит",
    "E621": "Мононатриев глутамат (Овкусител) - Може да причини главоболие.",
    "E951": "Аспартам (Подсладител) - Изкуствен подсладител, спорен за здравето."
}

def process_image(image):
    # Инициализиране на EasyOCR (за Български и Английски)
    reader = easyocr.Reader(['bg', 'en'])
    
    # Превръщане на изображението в подходящ формат
    img_array = np.array(image)
    
    # Извличане на текста
    results = reader.readtext(img_array, detail=0)
    return " ".join(results).upper()

# --- Интерфейс на Streamlit ---
st.set_page_config(page_title="Детектор на вредни съставки", page_icon="🧪")
st.title("🔍 Скенер за вредни съставки (E-номера)")
st.write("Качете снимка на етикета със съдържанието на продукта.")

uploaded_file = st.file_uploader("Изберете снимка...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Качена снимка', use_container_width=True)
    
    with st.spinner('Анализиране на текста... моля изчакайте.'):
        try:
            # 2. OCR разпознаване
            extracted_text = process_image(image)
            
            st.subheader("Разпознат текст:")
            st.info(extracted_text)
            
            # 3. Проверка за вредни съставки
            found_harmful = []
            for code, description in HARMFUL_INGREDIENTS.items():
                if code in extracted_text:
                    found_harmful.append((code, description))
            
            # 4. Показване на резултатите
            st.divider()
            if found_harmful:
                st.error(f"⚠️ Внимание! Открити са {len(found_harmful)} потенциално вредни съставки:")
                for code, desc in found_harmful:
                    st.warning(f"**{code}**: {desc}")
            else:
                st.success("✅ Не са открити познати вредни Е-номера в текста.")
                
        except Exception as e:
            st.error(f"Възникна грешка при обработката: {e}")
