import requests
import os

def get_ibm_token():
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "apikey": os.getenv("WATSONX_API_KEY"),
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to get IBM token: {response.text}")
