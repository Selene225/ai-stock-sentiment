import streamlit as st
import requests
from snownlp import SnowNLP

st.title("AI Stock News Sentiment Analyzer")

stock = st.text_input("Enter Stock Code", "000001")


def get_news():

    url = "https://feed.mix.sina.com.cn/api/roll/get"

    params = {
        "pageid": "153",
        "lid": "2509",
        "num": "10"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, params=params, headers=headers)

    data = r.json()

    news = []

    for item in data["result"]["data"]:
        news.append(item["title"])

    return news


def analyze(news):

    positive = 0
    negative = 0
    neutral = 0

    for n in news:

        s = SnowNLP(n)
        score = s.sentiments

        if score > 0.6:
            positive += 1
        elif score < 0.4:
            negative += 1
        else:
            neutral += 1

    return positive, negative, neutral


if st.button("Analyze"):

    news = get_news()

    st.subheader("Latest News")

    for n in news:
        st.write("-", n)

    pos, neg, neu = analyze(news)

    st.subheader("Sentiment Result")

    st.write("Positive:", pos)
    st.write("Negative:", neg)
    st.write("Neutral:", neu)

    if pos > neg:
        st.success("Overall Market Sentiment: Positive")
    elif neg > pos:
        st.error("Overall Market Sentiment: Negative")
    else:
        st.warning("Overall Market Sentiment: Neutral")