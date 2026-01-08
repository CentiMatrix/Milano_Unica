import os
import requests
import json
import time

APP_ID = "cli_a9af39f677385bde"
APP_SECRET = "ckBVL9AIh3A6mLXUrx9SwfcNvUxbIGAH"
APP_TOKEN = "XBk2bUZZxaw6UXsOq0EcietfnQf"
TABLE_ID = "tblfLrM2dD9yDjD8"

def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json().get("tenant_access_token")

def sync_records(token, records_data):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/batch_create"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    for i in range(0, len(records_data), 100):
        batch = records_data[i:i+100]
        payload = {
            "records": [{"fields": record} for record in batch]
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"Uploaded batch {i//100 + 1}. Status: {response.json().get('msg')}")
        else:
            print(f"Error uploading batch {i//100 + 1}: {response.text}")

if __name__ == "__main__":
    # 1. Load the parsed data
    data_path = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/Milano_Unica/scripts/mu_reports_data.json"
    with open(data_path, "r", encoding="utf-8") as f:
        parsed_data = json.load(f)
    
    records_to_upload = []
    for item in parsed_data:
        fields = {
            "品牌名称": item.get("品牌名称", ""),
            "核心提要": item.get("核心提要", ""),
            "展位号": item.get("展位号", ""),
            "核心品类": item.get("核心品类", ""),
            "核心优势": item.get("核心优势", ""),
            "价格区间": item.get("价格区间", ""),
            "调性分析": item.get("调性分析", "")
        }
        records_to_upload.append(fields)

    # 2. Get Auth Token
    token = get_tenant_access_token()
    if token:
        print("Auth Success.")
        sync_records(token, records_to_upload)
    else:
        print("Auth Failed.")
