import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# Зареждаме и кешираме OCR модела, за да не заема памет при всяко обновяване
@st.cache_resource
def load_model():
    # 'bg' за български, 'en' за английски
    return easyocr.Reader(['bg', 'en'], gpu=False)

def main():
    st.set_page_config(page_title="Health Scanner", page_icon="🥗")
    st.title("🥗 Скенер за вредни съставки")
    st.write("Качете снимка на етикет, за да проверим за вредни добавки.")

    # Списък за проверка
    HARMFUL = [
        "E621", "MSG", "monosodium glutamate", "мононатриев глутамат", 
        "палмово масло", "palm oil", "аспартам", "aspartame", 
        "хидрогенирани мазнини", "hydrogenated fat", "preservatives", "Guarana extract",  "E102", "E104", "E110","E122","E123", "E124", "E127", "E129", "E150C", "E150D",
        "E171", "E211", "E220",  "E221", "E222",  "E223",  "E224", "E228", "E249",  "E250", "E251",  "E252",  "E320",  "E321", "E407",  "E621",  "E950", "E951",  "E952", 
        "E954", "E955", "E999"
    ]

    reader = load_model()
    
    uploaded_file = st.file_uploader("Изберете изображение...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # Показваме снимката (новата версия на командата е с 'width')
        st.image(image, caption="Вашият етикет", width=500)
        
        with st.spinner('Анализиране на текста... Моля изчакайте.'):
            # Конвертиране за OCR
            img_np = np.array(image)
            results = reader.readtext(img_np, detail=0)
            full_text = " ".join(results).lower()

        st.subheader("Резултати от анализа:")
        
        found = [item for item in HARMFUL if item.lower() in full_text]

        if found:
            st.error(f"⚠️ Внимание! Открити съставки: {', '.join(found)}")
        else:
            st.success("✅ Не са открити опасни съставки от списъка.")
            
        with st.expander("Виж разпознатия текст"):
            st.write(full_text)

if __name__ == "__main__":
    main()
