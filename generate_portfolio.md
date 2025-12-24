# Portfolio JSON Rule

## 1. Portfolio JSON 구조

```json
{
  "config": {
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD"
  },
  "portfolios": {
    "current": {
      "config": { "interval": "monthly" },
      "tickers": [
        {
          "ticker": "AAPL",
          "name": "Apple Inc.",
          "weight": 0.5,
          "show": false
        },
        {
          "ticker": "USD",
          "name": "cash",
          "weight": 0.5,
          "show": false
        }
      ]
    },
    "target": {
      "config": { "interval": "monthly" },
      "tickers": [
        {
          "ticker": "AAPL",
          "name": "Apple Inc.",
          "weight": 0.7,
          "show": false
        },
        {
          "ticker": "USD",
          "name": "cash",
          "weight": 0.3,
          "show": false
        }
      ]
    }
  }
}
```

## 2. Key Rules
- **Portfolio Names**: keyword from requirement
- **Weights**: Use numbers (0.0 to 1.0). 0.01% = `0.0001`.
- **Show Flag**: Use boolean (true/false). default false
- **Cash**: Tickers `USD` or `KRW` are treated as cash (0% return).
- **Interval**: This is rebalance interval. Supports `none`, `weekly`, `monthly`, `quarterly`, `yearly`.

## 3. requirements
- Every portfolio has 2 tickers
  - QQQ 50%
  - USD 50%
- Each portfolios has different rebalance interval
  - none
  - weekly
  - monthly
  - quarterly
  - yearly