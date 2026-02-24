import streamlit as st
import google.generativeai as genai

# Page Setup - Matching your dark theme style
st.set_page_config(page_title="Burmese AI Pro", page_icon="🇲🇲")
st.title("🇲🇲 Burmese AI Pro")

# Sidebar for your API Key
api_key = st.sidebar.text_input("Enter Gemini API Key", value="AIzaSyB-gfM4w1RqICzzjFH2f5yAIen7kPCFFEw", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # Matching your tone buttons
    tone = st.radio("Select Tone", ["Comedy 😊", "Horror 💀", "Drama 🤍", "Action ⚡"], horizontal=True)

    uploaded_file = st.file_uploader("Upload English SRT File", type=['srt'])
    
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        st.text_area("English Preview", content, height=150)

        if st.button("🚀 Start Translation"):
            try:
                # Using the stable 1.5-flash model for Free Tier
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"Translate this movie script to natural Burmese with a {tone} style. Keep all SRT timestamps and numbers exactly the same: \n\n{content}"
                
                with st.spinner("AI is translating..."):
                    response = model.generate_content(prompt)
                    translated_text = response.text
                    
                    st.success("✅ Translation Complete!")
                    st.text_area("Burmese Result", translated_text, height=300)
                    
                    # Download Button
                    st.download_button(
                        label="📥 Download Burmese SRT",
                        data=translated_text,
                        file_name="translated_burmese.srt",
                        mime="text/plain"
                    )
            except Exception as e:
                st.error(f"❌ Error: {str(e)}. If in Thailand, try turning off your VPN.")
else:
    st.warning("Please enter your API Key in the sidebar to begin.")
                  
