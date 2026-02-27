import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Torrent Search", page_icon="🎬")

st.title("🎬 Torrent Movie Search")
query = st.text_input("Search for a movie", placeholder="Enter title...")

if query:
    with st.spinner('Searching...'):
        # Updated URL and better headers to avoid the timeout
        url = f"https://bitsearch.to/search?q={query}"
        
        # This makes the website think you are using a real Android phone
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        try:
            # We increased timeout to 20 seconds and added headers
            response = requests.get(url, headers=headers, timeout=20)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = soup.select('.search-result')

                if not results:
                    st.warning("No results found. Try a different movie name.")
                
                for item in results:
                    title = item.select_one('h5').text.strip()
                    # Safe check for magnet links
                    link_tag = item.find('a', href=lambda x: x and x.startswith('magnet'))
                    if link_tag:
                        magnet = link_tag['href']
                        stats = item.select('.stats div')
                        size = stats[2].text.strip() if len(stats) > 2 else "N/A"
                        
                        with st.expander(f"📥 {title}"):
                            st.write(f"**Size:** {size}")
                            st.code(magnet, language="markdown")
                            st.link_button("Open Magnet Link", magnet)
            else:
                st.error(f"Site is blocking us (Status Code: {response.status_code}). Try again in a minute.")
                
        except Exception as e:
            st.error("Connection too slow. Please try clicking search again.")
            
