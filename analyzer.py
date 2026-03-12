import requests
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# 获取新浪财经新闻
def get_stock_news(stock):
    url = f"https://finance.sina.com.cn/realstock/company/{stock}/finance.json"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    data = response.json()
    news = []

    for item in data["result"]:
        news.append(item["title"])

    return news

# 情绪分析
def analyze_sentiment(news_list):
    positive = 0
    negative = 0
    neutral = 0

    for headline in news_list:
        s = SnowNLP(headline)
        score = s.sentiments  # 0~1

        if score > 0.6:
            positive += 1
        elif score < 0.4:
            negative += 1
        else:
            neutral += 1

    return positive, negative, neutral

# 绘制情绪分布图
def plot_sentiment_distribution(positive, negative, neutral):
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [positive, negative, neutral]
    colors = ['#66b3ff', '#ff6666', '#c2c2f0']

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(labels, sizes, color=colors)
    ax.set_ylabel("Counts")
    ax.set_title("Sentiment Distribution")

    for i, v in enumerate(sizes):
        ax.text(i, v + 0.2, str(v), ha='center')

    plt.show()