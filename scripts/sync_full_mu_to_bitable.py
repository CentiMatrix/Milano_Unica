import os
import requests
import json
import re

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

def sync_full_mu(token):
    # 1. Load existing parsed intel (the 15 deep reports)
    intel_data_path = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/Milano_Unica/scripts/mu_reports_data.json"
    intel_lookup = {}
    if os.path.exists(intel_data_path):
        with open(intel_data_path, "r", encoding="utf-8") as f:
            for item in json.load(f):
                # Normalize name for matching
                intel_lookup[item.get("品牌名称", "").upper().strip()] = item

    # 2. Parse EXHIBITOR_LIST.md
    mu_list_path = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/Milano_Unica/EXHIBITOR_LIST.md"
    with open(mu_list_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex for table rows: | Name | Area | Hall | Stand |
    rows = re.findall(r'^\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|', content, re.MULTILINE)
    
    records_to_upload = []
    # Skip the header rows (Index 0 is header, 1 is separator)
    for i in range(2, len(rows)):
        name, area, hall, stand = rows[i]
        name = name.strip()
        if not name or name == "---": continue
        
        # Consolidate record
        fields = {
            "品牌名称": name,
            "类别": area.strip(),
            "展馆": hall.strip(),
            "展位号": stand.strip()
        }
        
        # Add deep intel if available
        norm_name = name.upper().strip()
        if norm_name in intel_lookup:
            intel = intel_lookup[norm_name]
            fields["核心提要"] = intel.get("核心提要", "")
            fields["核心品类"] = intel.get("核心品类", "")
            fields["核心优势"] = intel.get("核心优势", "")
            fields["价格区间"] = intel.get("价格区间", "")
            fields["调性分析"] = intel.get("调性分析", "")
        
        records_to_upload.append(fields)

    # 3. Batch Upload
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{TABLE_ID}/records/batch_create"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Batch size of 100
    for i in range(0, len(records_to_upload), 100):
        batch = records_to_upload[i:i+100]
        payload = {
            "records": [{"fields": r} for r in batch]
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"Uploaded batch {i//100 + 1}. Status: {response.json().get('msg')}")
        else:
            print(f"Error uploading batch {i//100 + 1}: {response.text}")

if __name__ == "__main__":
    token = get_tenant_access_token()
    if token:
        sync_full_mu(token)
    else:
        print("Auth failed.")
