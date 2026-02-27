import streamlit as st
import requests

st.set_page_config(page_title="Pro Torrent Search", page_icon="🎬")

st.title("🎬 Pro Torrent Search")
st.caption("Stable API Mode — Faster and No Blocks")

# Search Input
query = st.text_input("Enter Movie Name", placeholder="e.g. Stephen Chow")

if query:
    # 1. First we try a stable API
    with st.spinner('Fetching from Global Database...'):
        # This API is built for apps like yours
        api_url = f"https://torrent-api-py-interface.vercel.app/api/v1/all/{query}"
        
        try:
            response = requests.get(api_url, timeout=15)
            if response.status_code == 200:
                results = response.json()
                
                if not results or len(results) == 0:
                    st.warning("No direct results. Try the Google Search button below.")
                else:
                    for item in results[:15]: # Show top 15 results
                        title = item.get('title', 'Unknown Title')
                        magnet = item.get('magnet')
                        size = item.get('size', 'N/A')
                        seeds = item.get('seeds', '0')
                        
                        with st.expander(f"📦 {title}"):
                            st.write(f"**Size:** {size} | **Seeders:** {seeds}")
                            if magnet:
                                st.link_button("🧲 Get Magnet Link", magnet)
                                st.code(magnet, language="text")
            else:
                st.error("API is busy. Use the Manual Search button below.")
        except:
            # 2. If API fails, we provide a direct search button as a backup
            st.info("Direct connection is slow. Use this shortcut:")
            google_search = f"https://www.google.com/search?q={query}+site:bitsearch.to+OR+site:thepiratebay.org"
            st.link_button(f"🔍 Search for '{query}' on Google", google_search)

st.divider()
st.info("Tip: If 'Open Magnet Link' doesn't work, long-press the text code to copy it into your Torrent app (like Flud or LibreTorrent).")
            
