import requests
from twilio.rest import Client

STOCK
COMPANY_NAME
stock_api_key
news_api_key
account_sid
auth_token


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
def get_news():
    news_parameters={
        'q': COMPANY_NAME,
        'apiKey': news_api_key
    }
    news_data = requests.get(url='https://newsapi.org/v2/everything', params=news_parameters)
    top_3_news = news_data.json()['articles'][:3]
    top_3_titles = [news['title'] for news in top_3_news]
    top_3_descriptions = [news['description'] for news in top_3_news]
    send_message(top_3_titles, top_3_descriptions)


def send_message(titles: list, descriptions: list):
    message_to_send = f"{COMPANY_NAME}: {change_message}\n" \
                      f"Title: {titles[0]}\nBrief: {descriptions[0]}\n" \
                      f"Title: {titles[1]}\nBrief: {descriptions[1]}\n" \
                      f"Title: {titles[2]}\nBrief: {descriptions[2]}\n"
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=message_to_send,
        from_='+14707858749',
        to='receiver_phone_num'
    )
    print(message.status)

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': stock_api_key,
}
stock_data = requests.get(url='https://www.alphavantage.co/query', params=stock_parameters)
data = stock_data.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]
price_yesterday = float(data_list[0]['4. close'])
print(price_yesterday)
price_before_yesterday = float(data_list[1]['4. close'])
print(price_before_yesterday)
change_price = abs(price_yesterday-price_before_yesterday)
change_price = abs(price_yesterday-price_before_yesterday)
if price_yesterday>price_before_yesterday:
    change_message = f"🔺{round((change_price/price_before_yesterday)*100)}%"
else:
    change_message = f"🔻{round((change_price/price_before_yesterday)*100)}%"
if change_price/price_before_yesterday > 0.05:
    get_news()

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
