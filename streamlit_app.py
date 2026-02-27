import streamlit as st
import requests
from bs4 import BeautifulSoup

# App Page Config
st.set_page_config(page_title="Torrent Search", page_icon="🎬")

st.title("🎬 Torrent Movie Search")
query = st.text_input("Search for a movie (e.g., 'Deadpool')", placeholder="Enter title...")

if query:
    with st.spinner('Searching bitsearch.to...'):
        url = f"https://bitsearch.to/search?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.select('.search-result')

            if not results:
                st.warning("No results found.")
            
            for item in results:
                title = item.select_one('h5').text.strip()
                magnet = item.find('a', href=lambda x: x and x.startswith('magnet'))['href']
                stats = item.select('.stats div')
                size = stats[2].text.strip() if len(stats) > 2 else "N/A"
                seeds = stats[0].text.strip() if len(stats) > 0 else "0"

                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{title}**")
                        st.caption(f"Size: {size} | Seeders: {seeds}")
                    with col2:
                        st.link_button("🧲 Magnet", magnet)
                    st.divider()
        except Exception as e:
            st.error(f"Error connecting: {e}")
                
