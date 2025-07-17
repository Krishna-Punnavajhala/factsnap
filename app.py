import streamlit as st
import requests
from transformers import pipeline

API_KEY = st.secrets["API_KEY"]
# Load summarizer
@st.cache_resource(show_spinner=False)
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

# Fetch news from NewsAPI
def fetch_articles(topic):
    url = f"https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&language=en&apiKey=YOUR_API_KEY"
    response = requests.get(url)
    data = response.json()
    return data["articles"]

# Summarize the news article text
def summarize_text(text):
    max_chunk = 500
    text = text[:max_chunk]
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Streamlit UI
st.title("🧠 FactSnap")
topic = st.text_input("Enter a topic:")

if topic:
    articles = fetch_articles(topic)
    
    for article in articles:
        st.markdown(f"### [{article['title']}]({article['url']})")
        st.markdown(f"**Source:** {article['source']['name']}")
        st.markdown(f"**Published:** {article['publishedAt'][:10]}")
        
        description = article['description'] or article['content'] or ""
        
        if description:
            if st.button(f"Show summary for: {article['title'][:40]}..."):
                with st.spinner("Summarizing..."):
                    summary = summarize_text(description)
                    st.success(summary)
            else:
                st.write(description)
        else:
            st.write("No description available.")
        
        st.write("---")
