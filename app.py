import streamlit as st
import requests
from snownlp import SnowNLP

st.title("AI Stock Sentiment Analyzer")

stock = st.text_input("Enter Stock Code", "000001")


def get_stock_news():

    url = "https://feed.mix.sina.com.cn/api/roll/get"

    params = {
        "pageid": "153",
        "lid": "2509",
        "num": "10"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return []

    data = response.json()

    news = []

    for item in data["result"]["data"]:
        news.append(item["title"])

    return news


def analyze(news):

    positive = 0
    negative = 0
    neutral = 0

    results = []

    for headline in news:

        s = SnowNLP(headline)
        score = s.sentiments

        if score > 0.6:
            sentiment = "Positive"
            positive += 1

        elif score < 0.4:
            sentiment = "Negative"
            negative += 1

        else:
            sentiment = "Neutral"
            neutral += 1

        results.append((headline, sentiment, round(score,2)))

    return results, positive, negative, neutral


if st.button("Analyze"):

    st.write("Fetching news...")

    news = get_stock_news()

    if not news:
        st.write("Failed to fetch news")
    else:

        results, pos, neg, neu = analyze(news)

        st.subheader("News Sentiment")

        for r in results:
            st.write(r)

        st.subheader("Summary")

        st.write("Positive:", pos)
        st.write("Negative:", neg)
        st.write("Neutral:", neu)

        if pos > neg:
            overall = "Positive"
        elif neg > pos:
            overall = "Negative"
        else:
            overall = "Neutral"

        st.subheader("AI Conclusion")

        st.write("Market Sentiment:", overall)
        import openai

# 设置 API 密钥
openai.api_key = 'yuzuruchaos'

# 使用 OpenAI 来总结新闻
def summarize_news(news):
    response = openai.Completion.create(
        engine="text-davinci-003",  # 使用 Davinci 模型
        prompt=f"Summarize the following news: {news}",
        max_tokens=50,
        temperature=0.7  # 控制生成文本的随机性
    )
    return response.choices[0].text.strip()

# 在情绪分析中使用新闻总结
for headline in news:
    summary = summarize_news(headline)  # 调用新闻总结功能
    print("Summary:", summary)
    import matplotlib.pyplot as plt

# 绘制情绪分布图
def plot_sentiment_distribution(positive, negative, neutral):
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [positive, negative, neutral]
    
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # 确保饼图为圆形
    plt.title("Sentiment Distribution")
    plt.show()

# 在分析完所有新闻后调用图表
plot_sentiment_distribution(positive, negative, neutral)