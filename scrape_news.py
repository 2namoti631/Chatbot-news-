import requests
from bs4 import BeautifulSoup
import json

def get_news():
    url = 'https://vnexpress.net/khoa-hoc/khoa-hoc-trong-nuoc'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news = []
    articles = soup.find_all('article', class_='item-news')
    for article in articles:
        title_tag = article.find('h3', class_='title-news')
        summary_tag = article.find('p', class_='description')
        link_tag = article.find('a', href=True)

        if title_tag and summary_tag and link_tag:
            title = title_tag.text.strip()
            summary = summary_tag.text.strip()
            link = link_tag['href']
            news.append({'title': title, 'summary': summary, 'link': link})
    
    return news

def prepare_intents(news_data):
    intents = {"intents": []}
    for news in news_data:
        intents["intents"].append({
            "tag": news['title'],
            "patterns": [news['summary']],
            "responses": [f"Đây là tin tức mới nhất về: {news['title']}. Đọc thêm tại: {news['link']}"],
            "context": [""]
        })
    return intents

news_data = get_news()
news_intents = prepare_intents(news_data)

with open('Chatbot-news-\ news_data.json', 'w', encoding='utf-8') as file:
    json.dump(news_intents, file, ensure_ascii=False, indent=4)

print("Đã thu thập và xử lý dữ liệu tin tức")
