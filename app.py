import streamlit as st
from analyzer import get_stock_news, analyze_sentiment, plot_sentiment_distribution

def main():
    st.title("AI Stock Sentiment Analyzer")
    
    stock = st.text_input("请输入股票代码:")
    
    if stock:
        st.write("\n正在获取新闻...")

        news = get_stock_news(stock)

        if not news:
            st.write("获取新闻失败")
            return

        st.write("\n最新新闻:")
        for n in news:
            st.write("-", n)

        st.write("\n开始情绪分析...")

        positive, negative, neutral = analyze_sentiment(news)

        st.write("\n情绪统计")
        st.write(f"Positive: {positive}")
        st.write(f"Negative: {negative}")
        st.write(f"Neutral: {neutral}")

        # 绘制情绪分布图
        plot_sentiment_distribution(positive, negative, neutral)

        # 总体情绪
        if positive > negative:
            result = "Positive"
        elif negative > positive:
            result = "Negative"
        else:
            result = "Neutral"

        st.write("\nAI结论:")
        st.write(f"市场情绪: {result}")

if __name__ == "__main__":
    main()