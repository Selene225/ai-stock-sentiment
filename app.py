import streamlit as st
import matplotlib.pyplot as plt

from analyzer import (
    get_stock_price,
    get_kline,
    get_stock_news,
    analyze_sentiment,
    generate_report
)

st.title("AI Stock Analyzer")

stock = st.text_input("输入股票代码 (例如 000001 或 600519)")


if st.button("开始分析"):

    if not stock:
        st.warning("请输入股票代码")
        st.stop()

    price = get_stock_price(stock)

    if price:

        st.subheader("股票行情")

        col1, col2 = st.columns(2)

        col1.metric("价格", price["price"])
        col2.metric("涨跌幅", f"{price['change']}%")

    st.subheader("K线图")

    kline = get_kline(stock)

    closes = [float(i["close"]) for i in kline]

    st.line_chart(closes)

    st.write("正在获取新闻...")

    news = get_stock_news(stock)

    if not news:

        st.error("没有获取到新闻")

    else:

        st.subheader("新闻")

        for n in news:
            st.write("-", n)

        st.write("AI情绪分析中...")

        positive, negative, neutral, score = analyze_sentiment(news)

        st.subheader("情绪统计")

        labels = ["Positive", "Negative", "Neutral"]
        values = [positive, negative, neutral]

        fig, ax = plt.subplots()

        ax.bar(labels, values)

        st.pyplot(fig)

        st.subheader("Market Sentiment Score")

        st.metric("Sentiment Score", f"{score} / 10")

        if score > 7:
            advice = "Buy"
        elif score > 4:
            advice = "Hold"
        else:
            advice = "Risk"

        st.subheader("AI Investment Suggestion")

        st.write(advice)

        st.subheader("AI投资分析")

        report = generate_report(news)

        st.write(report)