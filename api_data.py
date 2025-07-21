from dotenv import load_dotenv
import os

load_dotenv()

key_name       = os.getenv("API_name")
key_secret     = os.getenv("API_secret")