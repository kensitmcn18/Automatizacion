# mews/utils.py
import requests

def safe_post(url, payload, headers):
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[ERROR] {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[EXCEPTION] Error calling {url}: {e}")
    return {}
