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
    # Fields for MU
    fields = [
        "品牌名称", "核心提要", "展位号", "核心品类", "核心优势", "价格区间", "调性分析"
    ]
    
    for f in fields:
        res = create_field(token, f, 1) # Type 1 is Text
        print(f"Created field {f}: {res.get('msg')}")
