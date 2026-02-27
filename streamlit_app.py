import streamlit as st
import urllib.parse

st.set_page_config(page_title="Torrent Search Hub", page_icon="🎬")

st.title("🎬 Movie Search Hub")
st.write("Since direct scraping is blocked, use these high-speed search buttons.")

# User Input
query = st.text_input("Enter Movie Name (e.g., Police Story)", placeholder="Type here...")

if query:
    encoded_query = urllib.parse.quote(query)
    
    st.subheader(f"Search results for: {query}")
    
    # We create direct links to the best search engines
    col1, col2 = st.columns(2)
    
    with col1:
        # Bitsearch Direct Link
        bit_url = f"https://bitsearch.to/search?q={encoded_query}"
        st.link_button("🔍 Search on Bitsearch", bit_url, use_container_width=True)
        
        # 1337x Direct Link
        x_url = f"https://1337x.to/search/{encoded_query}/1/"
        st.link_button("⚡ Search on 1337x", x_url, use_container_width=True)

    with col2:
        # Pirate Bay Proxy
        tpb_url = f"https://tpb.party/search/{encoded_query}/1/99/0"
        st.link_button("🏴‍☠️ Search PirateBay", tpb_url, use_container_width=True)
        
        # Google "Magnet" Hack
        google_url = f"https://www.google.com/search?q={encoded_query}+magnet+link+torrent"
        st.link_button("🌐 Google Magnet Search", google_url, use_container_width=True)

    st.info("Tip: Click a button above. When you find the movie, click the 'Magnet' icon and your Torrent app (Flud/LibreTorrent) will open automatically.")

st.divider()
st.caption("Built for Nyi Nyi Naing - Thailand 2026")
