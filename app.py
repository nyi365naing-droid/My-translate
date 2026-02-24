import streamlit as st
import google.generativeai as genai

# --- APP INTERFACE ---
st.set_page_config(page_title="Burmese AI Translator", page_icon="🇲🇲")
st.title("🇲🇲 Burmese AI Translator")
st.subheader("Human-like movie subtitles")

# Settings Sidebar
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    tone = st.selectbox("Select Movie Tone", ["Action", "Horror", "Comedy", "Drama", "Wuxia/Ancient"])
    st.info("Get a free key at aistudio.google.com")

uploaded_file = st.file_uploader("Upload English SRT File", type="srt")

if uploaded_file and api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if st.button("Start AI Translation"):
        lines = uploaded_file.getvalue().decode("utf-8").splitlines()
        translated_lines = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, line in enumerate(lines):
            # Only translate actual dialogue lines
            if any(c.isalpha() for c in line) and "-->" not in line:
                prompt = f"Translate this movie subtitle line into natural {tone} style Burmese. Use human-like conversational language. Only return the translated text: {line}"
                try:
                    response = model.generate_content(prompt)
                    translated_lines.append(response.text.strip() + "\n")
                except:
                    translated_lines.append(line + "\n")
            else:
                translated_lines.append(line + "\n")
            
            # Update progress
            progress_bar.progress((i + 1) / len(lines))
            if i % 10 == 0:
                status_text.text(f"Processing... {i} lines done.")
        
        final_srt = "".join(translated_lines)
        st.success("Translation Complete!")
        st.download_button("Download Burmese SRT", final_srt, file_name=f"Burmese_{tone}_{uploaded_file.name}")
