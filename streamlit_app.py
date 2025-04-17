import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from collections import Counter

# 안전하게 stopwords 다운로드
import nltk
def safe_nltk_download(resource):
    from nltk.data import find
    try:
        find(resource)
    except LookupError:
        nltk.download(resource)
safe_nltk_download('stopwords')

# UI
st.title("Trend Insight: English News Keyword Analyzer")
keyword = st.text_input("Enter search keyword (e.g., AI marketing)", "AI marketing")
num_articles = st.slider("Number of articles", 5, 50, 10)

# 뉴스 크롤링 함수
def fetch_news(keyword, num=10):
    headers = {"User-Agent": "Mozilla/5.0"}
    query = '+'.join(keyword.split())
    url = f"https://news.google.com/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = soup.find_all("a", class_="DY5T1d RZIKme", limit=num)
    return [{"title": a.text.strip()} for a in articles]

if keyword:
    news_data = fetch_news(keyword, num_articles)
    news_df = pd.DataFrame(news_data)

    st.subheader("Fetched News Titles")
    for title in news_df['title']:
        st.write("-", title)

    # 텍스트 분석
    all_text = " ".join(news_df['title'])
    tokens = all_text.split()
    tokens = [w.lower() for w in tokens if w.isalpha() and len(w) > 2]
    filtered = [w for w in tokens if w not in stopwords.words('english')]

    word_freq = Counter(filtered)

    # 시각화: WordCloud
    st.subheader("Word Cloud")
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

    # 시각화: 상위 키워드
    st.subheader("Top Keywords")
    top_words = word_freq.most_common(10)
    top_df = pd.DataFrame(top_words, columns=["Word", "Frequency"])
    st.bar_chart(top_df.set_index("Word"))