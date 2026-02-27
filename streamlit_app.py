import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

st.set_page_config(page_title="Stable Torrent Search", page_icon="🎬")

st.title("🎬 Stable Torrent Search")
st.caption("Anti-Block Mode (Google Search Method)")

query = st.text_input("Enter Movie Name", placeholder="e.g. Stephen Chow")

if query:
    with st.spinner('Finding stable links...'):
        # We search Google for the magnet link directly
        search_query = f"{query} site:bitsearch.to OR site:thepiratebay.org"
        url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                # Find all search result links
                links = soup.find_all("a")
                
                found = False
                for link in links:
                    href = link.get("href", "")
                    # Filter for actual movie page links
                    if "url?q=" in href and not "google.com" in href:
                        actual_url = href.split("url?q=")[1].split("&")[0]
                        title = link.text.replace("...", "").strip()
                        
                        if title and len(title) > 5:
                            st.write(f"📂 **{title}**")
                            st.link_button("View Torrent Page", actual_url)
                            found = True
                
                if not found:
                    st.warning("No links found. Try being more specific with the movie name.")
            else:
                st.error("Google is temporarily rate-limiting the app. Try again in 5 minutes.")
        except Exception as e:
            st.error("Connection too slow. Please refresh your browser tab.")
            
