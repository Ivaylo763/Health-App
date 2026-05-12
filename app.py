import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# Списък с вредни съставки (може да бъде разширен)
HARMFUL_INGREDIENTS = {
    "bg": ["E621", "мононатриев глутамат", "палмово масло", "хидрогенирани мазнини", "аспартам", "E951", "E211", "натриев бензоат"],
    "en": ["E621", "MSG", "monosodium glutamate", "palm oil", "hydrogenated fat", "aspartame", "E951", "E211", "sodium benzoate"]
}

st.set_page_config(page_title="Скенер за съставки", page_icon="🔍")

def main():
    st.title("🔍 Скенер за вредни съставки")
    st.write("Качете снимка на етикета със съдържанието, за да проверите за опасни добавки.")

    # Избор на език за OCR
    lang_option = st.selectbox(
        "Изберете език на етикета:",
        ("Български + Английски", "Само Английски")
    )
    
    reader_langs = ['bg', 'en'] if lang_option == "Български + Английски" else ['en']

    uploaded_file = st.file_uploader("Изберете снимка...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Качена снимка', use_container_width=True)
        
        with st.spinner('Разпознаване на текст... Моля изчакайте.'):
            # Инициализация на EasyOCR
            reader = easyocr.Reader(reader_langs, gpu=False) # Сменете на True, ако имате GPU
            
            # Конвертиране на PIL изображението в numpy array за EasyOCR
            image_np = np.array(image)
            results = reader.readtext(image_np, detail=0)
            
            full_text = " ".join(results).lower()
            
        st.subheader("Разпознат текст:")
        st.write(full_text)

        # Проверка за вредни съставки
        found_harmful = []
        all_checks = HARMFUL_INGREDIENTS["bg"] + HARMFUL_INGREDIENTS["en"]
        
        for ingredient in all_checks:
            if ingredient.lower() in full_text:
                if ingredient not in found_harmful:
                    found_harmful.append(ingredient)

        st.divider()

        # Показване на резултатите
        if found_harmful:
            st.error(f"⚠️ Внимание! Открити са потенциално вредни съставки:")
            for item in found_harmful:
                st.write(f"- **{item}**")
        else:
            st.success("✅ Не са открити съставки от черния списък.")

if __name__ == "__main__":
    main()
