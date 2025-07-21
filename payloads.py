


def create_order_sell_payload(client_order_id,product_id,base_size):

    payload = {
    "client_order_id": f"{client_order_id}",
    "product_id": f"{product_id}",
    "side": "SELL",
    "order_configuration": {
        "market_market_ioc": {
            
            "base_size": f"{base_size}",
            "rfq_disabled": True
        }
    }
    }

    return payload


def create_order_buy_payload(client_order_id,product_id,quote_size):

    payload = {
    "client_order_id": f"{client_order_id}",
    "product_id": f"{product_id}",
    "side": "BUY",
    "order_configuration": {
        "market_market_ioc": {
            "quote_size": f"{quote_size}",
           
            "rfq_disabled": True
        }
    }
    }

    return payload
