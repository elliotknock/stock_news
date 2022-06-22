import requests
from twilio.rest import Client

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = ""
NEWS_API_KEY = ""

TWILIO_SID = ""
TWILIO_AUTH_TOKEN = ""

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}

news_params = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]

stock_data_list = [close for (key, close) in stock_data.items()]

yesterday_data = stock_data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
day_before_yesterday_data = stock_data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

difference_percent = round((difference / float(yesterday_closing_price)) * 100)
if abs(difference_percent) > 5:
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    formatted_articles = [f"{STOCK}: {up_down}{difference_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}"
                          for article in three_articles]
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="",
            to=""
        )
