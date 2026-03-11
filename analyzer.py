import requests
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import os
import openai


# 读取API key
openai.api_key = os.getenv("OPENAI_API_KEY")


# 获取新浪财经新闻
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


# 情绪分析
def analyze_sentiment(news_list):

    positive = 0
    negative = 0
    neutral = 0

    for headline in news_list:

        s = SnowNLP(headline)
        score = s.sentiments

        print("\n新闻:", headline)
        print("情绪分数:", round(score, 2))

        if score > 0.6:
            positive += 1
            print("判断: Positive")

        elif score < 0.4:
            negative += 1
            print("判断: Negative")

        else:
            neutral += 1
            print("判断: Neutral")

    return positive, negative, neutral


# GPT总结新闻
def summarize_news(news):

    if not openai.api_key:
        return "No OpenAI API key provided."

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Summarize this financial news in one sentence: {news}",
        max_tokens=40
    )

    return response.choices[0].text.strip()


# 绘制情绪图
def plot_sentiment_distribution(positive, negative, neutral):

    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [positive, negative, neutral]

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title("News Sentiment Distribution")
    plt.axis('equal')

    plt.show()


# 主程序
def main():

    stock = input("输入股票代码: ")

    print("\n正在获取新闻...")

    news = get_stock_news()

    if not news:
        print("获取新闻失败")
        return

    print("\n最新新闻:")

    for n in news:
        print("-", n)

    print("\n新闻总结:")

    for n in news:
        summary = summarize_news(n)
        print("原新闻:", n)
        print("AI总结:", summary)

    print("\n开始情绪分析...")

    positive, negative, neutral = analyze_sentiment(news)

    print("\n情绪统计")
    print("Positive:", positive)
    print("Negative:", negative)
    print("Neutral:", neutral)

    # 总体结论
    if positive > negative:
        result = "Positive"
    elif negative > positive:
        result = "Negative"
    else:
        result = "Neutral"

    print("\nAI结论:")
    print("市场情绪:", result)

    # 画图
    plot_sentiment_distribution(positive, negative, neutral)


if __name__ == "__main__":
    main()