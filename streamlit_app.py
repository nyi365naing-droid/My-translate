import streamlit as st
import requests

# Page configuration
st.set_page_config(page_title="Burmese AI Pro", page_icon="🇲🇲")
st.title("🇲🇲 Burmese AI Pro")

# Sidebar for the API Key
api_key = st.sidebar.text_input("Gemini API Key", value="AIzaSyB-gfM4w1RqICzzjFH2f5yAIen7kPCFFEw", type="password")

if api_key:
    # Tone selection
    tone = st.radio("Select Style", ["Comedy 😊", "Horror 💀", "Drama 🤍", "Action ⚡"], horizontal=True)

    # File uploader
    uploaded_file = st.file_uploader("Upload English SRT", type=['srt'])
    
    if uploaded_file:
        english_text = uploaded_file.getvalue().decode("utf-8")
        st.text_area("Original Text (Preview)", english_text[:500], height=150)

        if st.button("🚀 Start Translation"):
            # UPDATED FOR FEB 2026: Using the stable gemini-2.5-flash model
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"Translate this movie script/SRT to natural Burmese with a {tone} tone. Keep all SRT timestamps and numbers exactly the same: \n\n{english_text}"
                    }]
                }]
            }
            
            with st.spinner("AI is translating..."):
                try:
                    response = requests.post(url, json=payload)
                    data = response.json()
                    
                    if "candidates" in data:
                        translated_text = data["candidates"][0]["content"]["parts"][0]["text"]
                        st.success("✅ Success!")
                        st.text_area("Burmese Translation", translated_text, height=300)
                        
                        st.download_button(
                            label="📥 Download Burmese SRT",
                            data=translated_text,
                            file_name="translated_burmese.srt",
                            mime="text/plain"
                        )
                    else:
                        # Show exact error from Google to help us fix it
                        error_msg = data.get('error', {}).get('message', 'Unknown Error')
                        st.error(f"Google Error: {error_msg}")
                except Exception as e:
                    st.error(f"Connection Error: {str(e)}")
else:
    st.warning("Please enter your API key in the sidebar.")
    
