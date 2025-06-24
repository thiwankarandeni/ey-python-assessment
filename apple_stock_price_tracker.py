from bs4 import BeautifulSoup
import requests
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

THRESHOLD_PERCENT = 1  # I have assumed the percentage change threshold for sending an email alert as 1%

# Fetch the webpage
def get_stock_price():
    
    url = 'https://finance.yahoo.com/quote/AAPL?p=AAPL'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        stock_price = soup.find("span", {"data-testid": "qsp-price"}).text
        stock_price = float(stock_price.replace(',', ''))  # Remove commas for consistency
        return stock_price
    except Exception as e:
        print(f"Error fetching stock price: {e}")
        return None

# Fetch the previous stock price from a CSV file
def get_previous_stock_price():
    try:
        df = pd.read_csv('stock_data.csv')
        aapl_row = df[df['Company'] == 'AAPL']
        if not aapl_row.empty:
            previous_price = aapl_row.iloc[0]['Price']
            return float(previous_price)
        else:
            print("No previous stock price found for AAPL.")
            return None
    except Exception as e:
        print(f"Error reading previous stock price: {e}")
        return None
    
# Send an email alert if the stock price changes significantly
def send_email_alert(stock_price, previous_price, difference, percentage_change):
    # Email credentials
    sender_email = "thiwankaxvii@gmail.com"
    receiver_email = "randenit@yahoo.com"
    password = "qoamdwvoxoldwqso"

    # Set up message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Apple Inc. (AAPL) Stock Price Alert"

    # Email body
    body = f"""
    Apple Inc. (AAPL) Stock Price Alert

    Current Stock Price: {stock_price}
    Previous Stock Price: {previous_price}
    Price Difference: {difference}
    Percentage Change: {percentage_change:.2f}%
    """
    message.attach(MIMEText(body, "plain"))

    # Connect to Gmail SMTP server
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    current_stock_price = get_stock_price()
    previous_stock_price = get_previous_stock_price()

    if current_stock_price is not None and previous_stock_price is not None:
        difference = current_stock_price - previous_stock_price
        percentage_change = (difference / previous_stock_price) * 100

        print(f"Previous Price: {previous_stock_price}, Current Price: {current_stock_price}, Difference: {difference}, Percentage Change: {percentage_change:.2f}%")

        if abs(percentage_change) >= THRESHOLD_PERCENT:
            send_email_alert(current_stock_price, previous_stock_price, difference, percentage_change)

if __name__ == "__main__":
    main()


