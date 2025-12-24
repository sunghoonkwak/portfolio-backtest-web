import json
import re
import os
from datetime import datetime, timedelta

MD_FILE = 'generate_portfolio.md'
TICKER_JSON = 'ticker.json'
OUTPUT_FILE = 'generated.json'

def load_ticker_names():
    names = {}
    if os.path.exists(TICKER_JSON):
        try:
            with open(TICKER_JSON, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data.get('ticker_list', []):
                    names[item['ticker'].upper()] = item['name']
        except Exception as e:
            print(f"Warning: Failed to load {TICKER_JSON}: {e}")
    return names

def parse_weight(val):
    val = val.strip()
    if val.endswith('%'):
        return float(val[:-1]) / 100.0
    try:
        return float(val)
    except:
        return 0.0

def generate_portfolio():
    if not os.path.exists(MD_FILE):
        print(f"Error: {MD_FILE} not found.")
        return

    with open(MD_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    req_match = re.search(r'## 3\. requirements(.*?)$', content, re.DOTALL | re.IGNORECASE)
    if not req_match:
        print("Error: '## 3. requirements' section not found.")
        return

    req_text = req_match.group(1)
    ticker_map = load_ticker_names()

    # 1. Parse Tickers and Weights
    # Look for lines starting with '-' under the tickers section
    tickers = []
    ticker_section = re.search(r'(?:tickers|assets).*?\n(.*?)(?=\n-|$)', req_text, re.DOTALL | re.IGNORECASE)
    asset_block = ticker_section.group(1) if ticker_section else req_text
    
    asset_matches = re.findall(r'-\s*([\w\.\-]+)\s+([\d\.%]+)', asset_block)
    for ticker, weight_str in asset_matches:
        ticker_upper = ticker.strip().upper()
        weight = parse_weight(weight_str)
        name = ticker_map.get(ticker_upper, ticker_upper)
        if ticker_upper in ['USD', 'KRW', 'CASH']: name = 'cash'
        
        tickers.append({
            "ticker": ticker_upper,
            "name": name,
            "weight": weight,
            "show": False
        })

    # 2. Parse Intervals
    intervals = []
    interval_block_match = re.search(r'interval.*?\n(.*?)(?=\n-|$)', req_text, re.DOTALL | re.IGNORECASE)
    if interval_block_match:
        intervals = re.findall(r'-\s*(\w+)', interval_block_match.group(1))
    
    if not intervals:
        intervals = ['monthly'] # Default fallback

    # 3. Generate Portfolios
    final_portfolios = {}
    for interval in intervals:
        interval = interval.strip().lower()
        final_portfolios[interval] = {
            "config": {"interval": interval},
            "tickers": tickers
        }

    # 4. Config (Dates)
    config = {
        "start_date": (datetime.now() - timedelta(days=366)).strftime('%Y-%m-%d'),
        "end_date": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    }
    date_matches = re.findall(r'(\w+_date):\s*([\d-]+)', req_text)
    for key, val in date_matches:
        config[key] = val

    output = {
        "config": config,
        "portfolios": final_portfolios
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated {OUTPUT_FILE} with {len(final_portfolios)} portfolios.")

if __name__ == "__main__":
    generate_portfolio()
