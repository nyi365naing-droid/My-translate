import streamlit as st
import requests

st.set_page_config(page_title="Fast Torrent Search", page_icon="🎬")

st.title("🎬 High-Speed Torrent Search")
st.caption("Using API Mode (Faster & More Reliable)")

query = st.text_input("Search for a movie", placeholder="e.g. Jackie Chan")

if query:
    with st.spinner('Fetching results...'):
        # Using SolidTorrent API which is much more stable than scraping
        api_url = f"https://solidtorrents.to/api/v1/search?q={query}&category=all"
        
        try:
            response = requests.get(api_url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])

                if not results:
                    st.warning("No movies found for that name.")
                
                for item in results:
                    title = item.get('title', 'No Title')
                    magnet = item.get('magnet')
                    size_bytes = item.get('size', 0)
                    # Convert bytes to GB or MB
                    size = f"{round(size_bytes / (1024**3), 2)} GB" if size_bytes > 1024**3 else f"{round(size_bytes / (1024**2), 2)} MB"
                    seeds = item.get('swarm', {}).get('seeders', 0)

                    with st.expander(f"🎬 {title}"):
                        st.write(f"**Size:** {size}")
                        st.write(f"**Seeders:** {seeds}")
                        if magnet:
                            st.link_button("🧲 Open Magnet Link", magnet)
                            st.code(magnet, language="markdown")
            else:
                st.error("The search service is busy. Please try again in a moment.")

        except Exception as e:
            st.error("Connection error. Please check your internet or try a different search term.")
            
