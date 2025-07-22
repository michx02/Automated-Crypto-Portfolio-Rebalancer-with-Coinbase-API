# Autobalancing-Crypto

This is a lightweight Python application that automatically rebalances a cryptocurrency portfolio based on predefined asset allocation weights. It connects to the Coinbase API to retrieve market data, calculate discrepancies in current allocation, and execute simulated trades to bring the portfolio back to its target distribution.

---

## 🚀 Features

- ✅ Connects to Coinbase for real-time crypto asset pricing.
- 📊 Calculates current portfolio weights based on fetched data.
- ♻️ Automatically rebalances based on defined target weights.
- 🧪 Designed for extensibility and simulation before real trade execution.
- 🔐 Keeps API keys and secrets out of version control using `.env`.

---

## 📁 Project Structure

Autobalancing-Crypto/
│
├── app.py               # Main script to run the rebalancer
├── api_data.py          # Retrieves market prices from Coinbase
├── assets_config.py     # Contains asset names and target weight config
├── aunthentication.py   # Handles authentication using Coinbase credentials
├── payloads.py          # Prepares request payloads for the API
├── _get_orderbook.py    # Gets the order book for price granularity
├── .gitignore           # Ensures secret files like .env are excluded



---

## ⚙️ How It Works

1. Define your target asset allocation in `assets_config.py`.
2. The script checks your current portfolio weights via Coinbase.
3. If there's a significant deviation, it suggests simulated buy/sell actions.
4. Logs and prints details of simulated or real trades.

---

## 🔐 API Key Safety

- API keys are not hardcoded.
- Create a `.env` file and add the following:

API_name=your_key_here
API_secret=your_secret_here


- Add `.env` to your `.gitignore` to avoid accidental commits.

---

## 🛠️ Dependencies

- `requests`
- `dotenv` (for loading API credentials securely)

Install all dependencies:
```bash
pip install -r requirements.txt
```

---

## 💡 Recommendations

- 🔄 **Fee Optimization**: This tool works best with a Coinbase One subscription or reduced-fee tier to minimize trading costs, especially when rebalancing frequently.
- 💵 **Ensure Sufficient USD Balance**: Before rebalancing, make sure your Coinbase account has enough USD to fund purchases. Otherwise, the first transactions may fail.
- 🧠 **Trade Order Logic**: The system sorts actions so that it sells excess assets **before** attempting any purchases. This ensures that there's available balance to execute buy orders properly.


---

## 🧑‍💻 Author
Built by Michael Mvano as part of a cryptocurrency project to explore algorithmic portfolio management.
