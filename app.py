import requests
from aunthentication import build_jwt

from payloads import create_order_sell_payload, create_order_buy_payload
from assets_config import TARGET_ALLOCATION, clean_base_size,is_trade_size_valid





'''
returns the "uuid" of the portfolio
DISCLAIMER: This functions returns the first element of a list
The list is a list of uuid of all your portfolios
This code assumed your portfolio is at index 0. 
'''
def get_portfolio_uuid():

    url= "https://api.coinbase.com/api/v3/brokerage/portfolios"

    request_method = "GET"
    request_host =  "api.coinbase.com/"
    request_path = "api/v3/brokerage/portfolios"

    headers = build_jwt(request_method=request_method, 
                        request_host=request_host, request_path=request_path)
    
    response = requests.get(url=url, headers=headers) #returns a list of dictionaries

    if response.status_code ==200: 
        return response.json()['portfolios'][0]['uuid']
    
    print("Could Not fetch portfolio_uuid. The status code is",response.status_code)
 



#Fetch current portfolio holdings
def get_portfolio():

    portfolio_uuid = get_portfolio_uuid()

    url= f"https://api.coinbase.com/api/v3/brokerage/portfolios/{portfolio_uuid}"

    request_method = "GET"
    request_host =  "api.coinbase.com/"
    request_path = f"api/v3/brokerage/portfolios/{portfolio_uuid}"

    headers = build_jwt(request_method=request_method, 
                        request_host=request_host, request_path=request_path)
    
    response = requests.get(url=url, headers=headers)

    portfolio_map = response.json()

    return portfolio_map

#returns the total portfolio balance in USD
def total_balance():

    portfolio_map = get_portfolio()
    return portfolio_map["breakdown"]["portfolio_balances"]["total_balance"]["value"]



#returns the current allocation, type dictionary (Map)
def get_allocations():

    portfolio_map = get_portfolio()

    current_allocation = {}

    spot_positions_array = portfolio_map["breakdown"]["spot_positions"]
    

    
    for positions in spot_positions_array:
        asset = positions["asset"]

        if asset in current_allocation:
            current_allocation[asset] += positions["allocation"]

        elif asset in TARGET_ALLOCATION:
            current_allocation[asset] = positions["allocation"]


    for key in TARGET_ALLOCATION:
        if key not in current_allocation:
            current_allocation[key] =0

    return current_allocation


#returns what to do to get crypto balanced
def rebalance_decision():
    
    current_allocation = get_allocations()
    print("Current Allocations are ", current_allocation)

    total_current_allocation = 0

    for asset in current_allocation:
        total_current_allocation += current_allocation[asset]

    price_balance = float(total_balance())

    action = {} # says what qnty to buy(+)/sell(-)

    for asset in current_allocation:

        diff = ((TARGET_ALLOCATION[asset] - 
                 current_allocation[asset]/total_current_allocation)) * price_balance
        action[asset] = float(diff)

    return action # says what qnty to buy(+)/sell(-)


#server time is used a client_order_id since the id has to be uniques
def get_server_time():

    time_url = "https://api.coinbase.com/api/v3/brokerage/time"

    time_response = requests.request("GET", time_url)
    time_json = time_response.json()


    return time_json['iso']+time_json['epochSeconds']+time_json['epochMillis']

#Returns the value of the asset
def get_asset_price(asset):

    url = f"https://api.coinbase.com/api/v3/brokerage/market/products/{asset}-USD"

    response = requests.request("GET", url)
    price =float(response.json()["price"])

    return price


#buys/ sells asset in USD
def place_order(asset, side, usd_size):

    url = "https://api.coinbase.com/api/v3/brokerage/orders"

    request_method = "POST"
    request_host =  "api.coinbase.com/"
    request_path = "api/v3/brokerage/orders"

    headers = build_jwt(request_method=request_method, 
                        request_host=request_host, request_path=request_path)
    
    client_order_id = get_server_time()
    product_id = f'{asset}-USD'

    if side == "SELL":
        asset_price = get_asset_price(asset=asset)
        raw_base_size = usd_size/asset_price
        base_size = clean_base_size(asset, raw_base_size)

        payload =create_order_sell_payload(client_order_id=client_order_id,
                                        product_id=product_id,base_size = base_size)
        
        response = requests.request("POST", url, json=payload, headers=headers)

        if response.status_code == 200 :
            print(f"Sold ${usd_size} worth of {asset}")
            

        else:
            print(f"Error Selling {asset}, API Error code: {response.status_code}")
            

        

    if side == "BUY":
        usd_size = round(usd_size,2)
        payload = create_order_buy_payload(client_order_id=client_order_id,
                                        product_id=product_id,quote_size = usd_size)
        
        response = requests.request("POST", url, json=payload, headers=headers)

        if response.status_code == 200 :
            print(f"Bought ${usd_size} worth of {asset}")
            

        else:
            print(f"Error Buying {asset}, API Error code: {response.status_code}")


#places order to rebalance
def place_order_rebalance():

    decisions = rebalance_decision()
    print("Actions map(dictionary) is",decisions)

    for asset in decisions:
        usd_size =decisions[asset]

        if (usd_size < 0) and is_trade_size_valid(asset,usd_size*-1):
            usd_size *= -1 
            place_order(asset=asset,side="SELL",usd_size=round(usd_size,2))

        elif usd_size> 0 and is_trade_size_valid(asset, usd_size):
            place_order(asset=asset,side="BUY",usd_size=round(usd_size,2))

        else:
            print(f"Didn't place order for {asset}")

  

def main():   
    place_order_rebalance()


if __name__ == "__main__":
    main()