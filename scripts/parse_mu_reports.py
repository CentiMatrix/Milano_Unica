import os
import re
import json

def parse_intel_report(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    data = {}
    
    # Extract Title (Brand Name)
    title_match = re.search(r'# Master Mastery: (.+?) Intelligence Report', content)
    if not title_match:
        title_match = re.search(r'# (.+)', content)
        
    data['品牌名称'] = title_match.group(1).strip() if title_match else os.path.basename(filepath).replace('_intel.md', '').replace('_', ' ')

    # Extract Master Summary
    summary_match = re.search(r'## 💎 Executive Summary / 核心提要\n(.*?)\n---', content, re.DOTALL)
    if summary_match:
        data['核心提要'] = summary_match.group(1).strip()

    # Basic Info
    booth_match = re.search(r'- \*\*Booth / 展位\*\*: (.+)', content)
    data['展位号'] = booth_match.group(1).strip() if booth_match else ""
    
    products_match = re.search(r'- \*\*Key Categories / 核心品类\*\*: (.+)', content)
    data['核心品类'] = products_match.group(1).strip() if products_match else ""

    # B2B & Commercial Insights
    b2b_match = re.search(r'## 🎯 B2B & Commercial Insights / 商业见解\n(.*?)\n---', content, re.DOTALL)
    if b2b_match:
        data['核心优势'] = b2b_match.group(1).strip()

    # Pricing (Often under Pricing or Commercial Insights in MU reports)
    # The MU reports I generated have specific sections. Let's look for Pricing.
    pricing_match = re.search(r'## 💰 Pricing & Commercial Details / 定价与商业细节\n(.*?)\n---', content, re.DOTALL)
    if pricing_match:
        data['价格区间'] = pricing_match.group(1).strip()

    # Vibe Check
    vibe_match = re.search(r'## 💡 Vibe Check / 调性分析\n(.*?)\n---', content, re.DOTALL)
    if not vibe_match:
        vibe_match = re.search(r'## 💡 Vibe Check\n(.*?)$', content, re.DOTALL)
    if vibe_match:
        data['调性分析'] = vibe_match.group(1).strip()

    return data

def get_mu_reports(directory):
    reports = []
    files = [
        "Albiate_1830", "Albini_1876", "Angelico", "Botto_Giuseppe", "Canepa", 
        "Drago", "Ermenegildo_Zegna", "Lanificio_Colombo", "Loro_Piana", 
        "Piacenza_1733", "Reda_1865", "Solbiati", "Tessitura_di_Novara", 
        "Thomas_Mason", "Vitale_Barberis_Canonico"
    ]
    
    for brand in files:
        path = os.path.join(directory, f"{brand}_intel.md")
        if os.path.exists(path):
            reports.append(parse_intel_report(path))
        else:
            print(f"Warning: File not found {path}")
            
    return reports

if __name__ == "__main__":
    MU_DIR = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/Milano_Unica"
    all_data = get_mu_reports(MU_DIR)
    
    # Save to JSON for debugging
    with open("mu_reports_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"Parsed {len(all_data)} Milano Unica reports.")
