import yfinance as yf
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TICKER_JSON_PATH = os.path.join(BASE_DIR, 'ticker.json')

def load_tickers():
    if not os.path.exists(TICKER_JSON_PATH):
        return {"ticker_list": []}
    try:
        with open(TICKER_JSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading ticker.json: {e}")
        return {"ticker_list": []}

def save_tickers(data):
    try:
        with open(TICKER_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving ticker.json: {e}")
        return False

def get_ticker_info(symbol):
    symbol = symbol.upper()
    data = load_tickers()
    ticker_list = data.get('ticker_list', [])

    # Check if exists
    for item in ticker_list:
        if item['ticker'] == symbol:
            return item

    # If not found, fetch from yfinance
    try:
        print(f"Fetching data for {symbol} from yfinance...")
        yf_ticker = yf.Ticker(symbol)
        
        info = {}
        try:
            info = yf_ticker.info
        except Exception as e:
            print(f"Error getting .info for {symbol}: {e}")

        # Fallback to fast_info if main info is empty
        if not info or len(info) < 5:
            print(f"Main info for {symbol} is empty, trying fast_info...")
            try:
                fi = yf_ticker.fast_info
                info = {
                    'shortName': symbol,
                    'quoteType': fi.get('quoteType', 'Unknown'),
                    'currency': fi.get('currency', 'USD')
                }
            except Exception as e:
                print(f"Error getting fast_info for {symbol}: {e}")

        if not info or len(info) < 2:
            print(f"Detailed info for {symbol} not available, trying download check...")
            temp_df = yf.download(symbol, period="1d", progress=False)
            if temp_df.empty:
                print(f"Ticker {symbol} NOT found on yfinance via download.")
                return None
            info = {'shortName': symbol, 'quoteType': 'Unknown', 'currency': 'USD'}

        short_name = info.get('shortName') or info.get('longName') or symbol
        quote_type = info.get('quoteType', 'Unknown')
        currency = info.get('currency', 'USD')

        new_entry = {
            "name": short_name,
            "type": quote_type,
            "ticker": symbol,
            "currency": currency
        }

        # Update json
        ticker_list.append(new_entry)
        data['ticker_list'] = ticker_list
        if save_tickers(data):
            print(f"Successfully SAVED {symbol} to ticker.json")
        else:
            print(f"FAILED to save {symbol} to ticker.json")

        return new_entry

    except Exception as e:
        print(f"Global error in get_ticker_info for {symbol}: {e}")
        return None
