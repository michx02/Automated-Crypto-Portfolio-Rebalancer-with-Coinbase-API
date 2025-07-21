#Adjust the file per your Assets Needs 
#Always check symbol-specific rules from Coinbase trading rules API


TARGET_ALLOCATION = {
    "BTC": 0.4,
    "DOGE": 0.3,
    "SHIB" : 0.3
}


#puts the base_size in the right format
def clean_base_size(symbol, value):
    if symbol == 'SHIB':
        return str(int(value))
    elif symbol == 'DOGE':
        return f"{round(value, 2):.2f}"
    else:  # BTC, etc.
        return f"{round(value, 6):.6f}"
    



def is_trade_size_valid(symbol, quote_usd):
    min_size = {
        'BTC': 2.0,
        'DOGE': 1.0,
        'SHIB': 0.01
    }
    return quote_usd >= min_size.get(symbol, 1.0)
