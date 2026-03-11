import requests
from snownlp import SnowNLP

# 获取新浪新闻
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
        score = s.sentiments   # 0~1

        print("\n新闻:", headline)
        print("情绪分数:", round(score,2))

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

    print("\n开始情绪分析...")

    positive, negative, neutral = analyze_sentiment(news)

    print("\n情绪统计")
    print("Positive:", positive)
    print("Negative:", negative)
    print("Neutral:", neutral)

    # 总体情绪
    if positive > negative:
        result = "Positive"
    elif negative > positive:
        result = "Negative"
    else:
        result = "Neutral"

    print("\nAI结论:")
    print("市场情绪:", result)


if __name__ == "__main__":
    main()
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