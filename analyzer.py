import requests
import os
import feedparser
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

headers = {
    "User-Agent": "Mozilla/5.0"
}


# 股票行情（新浪）
def get_stock_price(code):

    if code.startswith("6"):
        url = f"https://hq.sinajs.cn/list=sh{code}"
    else:
        url = f"https://hq.sinajs.cn/list=sz{code}"

    r = requests.get(url, headers=headers)

    data = r.text.split(",")

    if len(data) < 5:
        return None

    name = data[0].split('"')[1]
    last_close = float(data[2])
    current_price = float(data[3])

    change = (current_price - last_close) / last_close * 100

    return {
        "name": name,
        "price": current_price,
        "change": round(change, 2)
    }


# K线
def get_kline(code):

    if code.startswith("6"):
        symbol = "sh" + code
    else:
        symbol = "sz" + code

    url = "https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData"

    params = {
        "symbol": symbol,
        "scale": 240,
        "ma": "no",
        "datalen": 50
    }

    r = requests.get(url, params=params, headers=headers)

    return r.json()


# 新闻（Google News RSS）
def get_stock_news(code):

    stock_map = {
        "000001": "平安银行",
        "600519": "贵州茅台",
        "601318": "中国平安",
        "600036": "招商银行"
    }

    keyword = stock_map.get(code, code)

    url = f"https://news.google.com/rss/search?q={keyword}&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"

    feed = feedparser.parse(url)

    news = []

    for entry in feed.entries[:10]:
        news.append(entry.title)

    return news


# AI情绪分析
def analyze_sentiment(news_list):

    positive = 0
    negative = 0
    neutral = 0

    for headline in news_list:

        prompt = f"""
判断下面财经新闻情绪，只返回：

positive
negative
neutral

新闻：
{headline}
"""

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        result = response.choices[0].message.content.strip().lower()

        if "positive" in result:
            positive += 1
        elif "negative" in result:
            negative += 1
        else:
            neutral += 1

    score_raw = (positive - negative) / max(len(news_list), 1)

    sentiment_score = round((score_raw + 1) * 5, 1)

    return positive, negative, neutral, sentiment_score


# AI投资报告
def generate_report(news_list):

    text = "\n".join(news_list)

    prompt = f"""
以下是股票相关新闻：

{text}

请生成投资分析：

1 市场情绪
2 投资机会
3 风险提示
4 结论
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content