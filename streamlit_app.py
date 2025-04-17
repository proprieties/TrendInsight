import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk

# NLTK resources download
nltk.download("punkt")
nltk.download("stopwords")

# ----------- News Fetching Function -----------
def fetch_news(keyword, num=10):
    headers = {"User-Agent": "Mozilla/5.0"}
    query = '+'.join(keyword.split())
    url = f"https://news.google.com/search?q={query}&hl=en-US&gl=US&ceid=US:en"

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    articles = soup.find_all("a", class_="DY5T1d RZIKme", limit=num)

    # Debug: If structure changes or articles not found
    if not articles:
        st.info("No articles found. The page structure may have changed or the keyword yielded no results.")

    return [{"title": a.text.strip()} for a in articles]

# ----------- Streamlit App UI -----------
st.set_page_config(page_title="Trend Insight: English News Keyword Analyzer", layout="centered")

st.title("Trend Insight: English News Keyword Analyzer")
st.markdown("Search the latest news based on a keyword and visualize keyword frequency + word cloud.")

# Keyword Input
keyword = st.text_input("Enter search keyword (e.g., AI marketing)", value="AI marketing")

# Number of articles slider
num_articles = st.slider("Number of articles", min_value=5, max_value=50, value=10)

# Fetch and Display News
if st.button("Analyze"):
    with st.spinner("Fetching news..."):
        news_data = fetch_news(keyword, num_articles)

    if not news_data:
        st.warning("No news data available. Try another keyword.")
    else:
        news_df = pd.DataFrame(news_data)

        st.subheader("Fetched News Titles")
        for title in news_df['title']:
            st.write("-", title)

        # Text processing
        all_text = " ".join(news_df['title']).lower()
        tokens = word_tokenize(all_text)
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]

        # Frequency count
        freq_dist = pd.Series(filtered_tokens).value_counts()

        st.subheader("Top Keywords")
        st.dataframe(freq_dist.head(20).reset_index().rename(columns={'index': 'Word', 0: 'Count'}))

        # Word cloud
        st.subheader("Word Cloud")
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(filtered_tokens))
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)