
import requests
from util import safe_post

class MewsClient:
    """
    mews_client.py es la responsable de conectarse a la API de Mews
    """
    def __init__(self, api_base_url, client_token, access_token):
        self.api_base_url = api_base_url
        self.client_token = client_token
        self.access_token = access_token
        self.headers = {"Content-Type": "application/json"}

    def post(self, endpoint: str, payload: dict) -> dict:
        url = f"{self.api_base_url}/{endpoint}"
        return safe_post(url, payload, self.headers)
