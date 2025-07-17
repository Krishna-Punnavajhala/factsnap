# app.py
import streamlit as st
import requests

# ----- PAGE CONFIG -----
st.set_page_config(page_title="FactSnap", layout="centered")

# ----- HEADER -----
st.title("🧠 FactSnap")
st.subheader("Filter out the BS. Get the real story.")
st.markdown("Enter a news topic to explore real-time news articles:")

# ----- USER INPUT -----
topic = st.text_input("🔍 Search Topic", placeholder="e.g. Ukraine, AI regulation, Climate change")

# ----- FUNCTION TO FETCH NEWS -----
def fetch_articles(query):
    api_key = "YOUR_API_KEY"  # 🔑 Replace this with your key
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&pageSize=5&sortBy=publishedAt&apiKey={api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["articles"]
    else:
        st.error("❌ Failed to fetch news. Check your API key or try again later.")
        return []

# ----- DISPLAY RESULTS -----
if topic:
    with st.spinner("Fetching the latest news..."):
        articles = fetch_articles(topic)

    if not articles:
        st.warning("No articles found. Try a different topic.")

    for article in articles:
        st.markdown(f"### [{article['title']}]({article['url']})")
        st.markdown(f"**📰 Source:** {article['source']['name']}")
        st.markdown(f"**📅 Published:** {article['publishedAt'][:10]}")
        st.write(article['description'])
        st.write("---")
