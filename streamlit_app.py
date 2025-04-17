# streamlit_trend_insight_en.py

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 다운로드 (최초 1회)
nltk.download('punkt')
nltk.download('stopwords')

st.set_page_config(page_title="Trend Insight Dashboard (EN)", layout="wide")

st.title("Trend Insight: English News Keyword Analyzer")
st.markdown("Search the latest news based on a keyword and visualize keyword frequency + word cloud.")

# 1. Keyword Input
keyword = st.text_input("Enter search keyword (e.g., AI marketing)", "AI marketing")
num_articles = st.slider("Number of articles", 5, 50, 10)

# 2. Google News Scraper (EN)
@st.cache_data
def collect_news(query, count):
    base_url = f"https://news.google.com/search?q={query}&hl=en&gl=US&ceid=US:en"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    titles = []
    for article in soup.select('article')[:count]:
        a_tag = article.find('a')
        if a_tag:
            titles.append(a_tag.text.strip())
    return pd.DataFrame({'title': titles})

# 3. Start Button
if st.button("Fetch News & Analyze"):
    news_df = collect_news(keyword, num_articles)

    st.subheader("Fetched News Titles")
    st.dataframe(news_df)

    all_text = " ".join(news_df['title'])
    tokens = word_tokenize(all_text)
    tokens = [w.lower() for w in tokens if w.isalpha() and len(w) > 2]
    filtered = [w for w in tokens if w not in stopwords.words('english')]

    word_freq = Counter(filtered)

    # 4. Keyword Frequency Bar Chart
    st.subheader("Top 10 Frequent Keywords")
    freq_df = pd.DataFrame(word_freq.most_common(10), columns=['Keyword', 'Frequency'])
    st.bar_chart(freq_df.set_index('Keyword'))

    # 5. WordCloud
    st.subheader("Word Cloud")
    wc = WordCloud(background_color='white', width=800, height=400)
    wc_img = wc.generate_from_frequencies(word_freq)
    st.image(wc_img.to_array(), use_column_width=True)