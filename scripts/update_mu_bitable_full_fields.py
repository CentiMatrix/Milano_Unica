import os
import requests
import json

APP_ID = "cli_a9af39f677385bde"
APP_SECRET = "ckBVL9AIh3A6mLXUrx9SwfcNvUxbIGAH"
APP_TOKEN = "XBk2bUZZxaw6UXsOq0EcietfnQf"
TABLE_ID = "tblfLrM2dD9yDjD8"

def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": APP_ID, "app_secret": APP_SECRET}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json().get("tenant_access_token")

def create_field(token, field_name, field_type):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/fields"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "field_name": field_name,
        "type": field_type
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

if __name__ == "__main__":
    token = get_tenant_access_token()
    # Adding new fields for full list
    fields = ["类别", "展馆"]
    for f in fields:
        res = create_field(token, f, 1) # Text
        print(f"Created field {f}: {res.get('msg')}")
