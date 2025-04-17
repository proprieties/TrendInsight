# streamlit_trend_insight_app.py

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

nltk.download('punkt')
nltk.download('stopwords')

st.set_page_config(page_title="트렌드 분석 대시보드", layout="wide")

st.title("트렌드 분석 및 시장 조사 솔루션")
st.markdown("키워드 기반 뉴스 기사 수집 및 트렌드 인사이트 시각화를 제공합니다.")

# 1. 키워드 입력
keyword = st.text_input("검색 키워드 입력 (예: AI 마케팅)", "AI 마케팅")
num_articles = st.slider("기사 수 (최대 50)", 5, 50, 10)

# 2. 뉴스 수집 함수
@st.cache_data
def collect_news_data(query, count=10):
    base_url = f"https://news.google.com/search?q={query}&hl=ko&gl=KR&ceid=KR%3Ako"
        headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(base_url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')

                    titles = []
                        for article in soup.select('article')[:count]:
                                title_tag = article.find('a')
                                        if title_tag:
                                                    titles.append(title_tag.text.strip())
                                                        return pd.DataFrame({'title': titles})

                                                        # 3. 버튼 클릭 시 뉴스 수집
                                                        if st.button("트렌드 뉴스 수집"):
                                                            news_df = collect_news_data(keyword, count=num_articles)
                                                                st.subheader("수집된 뉴스 제목")
                                                                    st.dataframe(news_df)

                                                                        # 4. 키워드 분석
                                                                            all_text = " ".join(news_df['title'])
                                                                                tokens = word_tokenize(all_text)
                                                                                    tokens = [w for w in tokens if w.isalpha() and len(w) > 1]
                                                                                        stop_words = set(stopwords.words('korean'))
                                                                                            filtered = [w for w in tokens if w not in stop_words]
                                                                                                word_freq = Counter(filtered)

                                                                                                    # 5. 시각화
                                                                                                        st.subheader("키워드 빈도 상위 10개")
                                                                                                            freq_df = pd.DataFrame(word_freq.most_common(10), columns=['단어', '빈도'])
                                                                                                                st.bar_chart(freq_df.set_index('단어'))

                                                                                                                    st.subheader("워드클라우드")
                                                                                                                        wc = WordCloud(font_path='NanumGothic.ttf', background_color='white', width=800, height=400)
                                                                                                                            wc_img = wc.generate_from_frequencies(word_freq)

                                                                                                                                st.image(wc_img.to_array(), use_column_width=True)