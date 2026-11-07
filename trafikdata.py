import requests
import os
api_key = os.environ.get("TRAFIKVERKET_API_KEY")
print("Rattantid startar")
print("API_nyckel hittad" if api_key else "API-nyckel saknas")
