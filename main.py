from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json(filename):
    try:
        file_path = os.path.join(BASE_DIR, filename)
        if not os.path.exists(file_path):
            return None
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/init-data')
def get_init_data():
    default_data = load_json('default.json')
    ticker_data = load_json('ticker.json')
    
    if default_data is None:
        default_data = {"assets": []}
    if ticker_data is None:
        ticker_data = {"ticker_list": []}

    return jsonify({
        'default': default_data,
        'tickers': ticker_data
    })

@app.route('/api/ticker/<symbol>')
def get_ticker(symbol):
    from ticker import get_ticker_info
    info = get_ticker_info(symbol)
    if info:
        return jsonify(info)
    else:
        return jsonify({"error": "Ticker not found"}), 404

@app.route('/api/run-backtest', methods=['POST'])
def run_backtest():
    from backtest import run_backtest_logic
    data = request.json
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    portfolios = data.get('portfolios')
    selected_tickers = data.get('selected_tickers', [])
    
    results = run_backtest_logic(start_date, end_date, portfolios, selected_tickers)
    return jsonify(results)

@app.route('/api/download-results')
def download_results():
    from flask import send_file
    file_path = os.path.join(BASE_DIR, 'backtest_results.xlsx')
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
