import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Torrent Search", page_icon="🎬")

st.title("🎬 Movie Torrent Search")
st.caption("Anti-Block Version (using TPB Proxy)")

query = st.text_input("Search for a movie", placeholder="e.g. Shaolin Soccer")

if query:
    with st.spinner('Searching...'):
        # Using a PirateBay proxy which is more stable for cloud servers
        search_url = f"https://tpb.party/search/{query}/1/99/0"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            response = requests.get(search_url, headers=headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # PirateBay results are in a table row <tr>
                rows = soup.select('tr')[1:]  # Skip the header row

                if not rows:
                    st.warning("No results found. Try another movie name.")

                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) > 1:
                        title_div = cols[1].find('div', class_='detName')
                        if title_div:
                            title = title_div.text.strip()
                            magnet = cols[1].find('a', href=lambda x: x and x.startswith('magnet'))['href']
                            desc = cols[1].find('font', class_='detDesc').text.strip()
                            
                            # Clean up the description to get just the size
                            size = desc.split(',')[1].replace('Size ', '') if ',' in desc else "Unknown"

                            with st.expander(f"📦 {title}"):
                                st.write(f"**Size:** {size}")
                                st.link_button("🧲 Get Magnet Link", magnet)
            else:
                st.error(f"Access denied (Status: {response.status_code}). Please try again.")

        except Exception as e:
            st.error("Search engine is currently offline. Trying to reconnect...")
            
