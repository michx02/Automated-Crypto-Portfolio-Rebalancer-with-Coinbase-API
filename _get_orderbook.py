import requests
from aunthentication import build_jwt

#To Get OrderBook, returns a list
def get_orderbook():

    url= "https://api.coinbase.com/api/v3/brokerage/orders/historical/batch"

    request_method = "GET"
    request_host = "api.coinbase.com/"
    request_path = "api/v3/brokerage/orders/historical/batch"
    

    #Authenticate
    headers = build_jwt(request_method, request_host, request_path)

    #Fetch for orders
    orders = requests.get(url=url, headers=headers)

    #Check if we got something from the servers
    if orders.status_code == 200 :
        return orders.json()

    #if not raise the error
    print("There was an Error Getting the orderBook")
    return []


def main():   
    print(get_orderbook()["orders"])


if __name__ == "__main__":
    main()

