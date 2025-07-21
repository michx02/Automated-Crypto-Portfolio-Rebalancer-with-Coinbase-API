import jwt
from cryptography.hazmat.primitives import serialization
import time
import secrets
import api_data


#For Authentication
def build_jwt(request_method, request_host, request_path):
    uri = f"{request_method} {request_host}{request_path}"
    private_key_bytes = api_data.key_secret.encode('utf-8')
    private_key = serialization.load_pem_private_key(private_key_bytes, password=None)
    jwt_payload = {
        'sub': api_data.key_name,
        'iss': "cdp",
        'nbf': int(time.time()),
        'exp': int(time.time()) + 120,
        'uri': uri,
    }
    jwt_token = jwt.encode(
        jwt_payload,
        private_key,
        algorithm='ES256',
        headers={'kid': api_data.key_name, 'nonce': secrets.token_hex()},
    )

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    return headers