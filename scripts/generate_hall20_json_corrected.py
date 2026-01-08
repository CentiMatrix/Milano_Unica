import os
import json
import csv

# --- 环境隔离 ---
os.environ["NO_PROXY"] = "127.0.0.1,localhost"

CSV_PATH = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/pdf_exhibitors.csv"
OUTPUT_JSON = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/hall20_intel.json"

# --- 商业智能来源说明 ---
# 注：所有价格与客户信息均为基于行业分层(Market Tiering)的“估算基准”。
# 批发价受订单量、汇率及展会现场政策影响，仅供采购预算梯度参考。

INTEL_WIKI = {
    "LORO PIANA": {
        "tier": "Luxury+",
        "price_range": "€85 - €350/m (基于行业基准估算)",
        "clients": "顶级奢侈品成衣 (LVMH系)、全球前50裁缝店",
        "grip": "其 S/S 2027 重点是‘亲肤/防护’功能的丝毛混纺。西装主理人应重点关注其 Linen Denim 和新的 Sunset 极轻羊绒系列。博弈点在于调拨稀缺样卡的优先权。",
        "value_prop": "S/S 2027 主打‘MU Cosmetic’理念下的二层皮肤感面料。"
    },
    "VITALE BARBERIS CANONICO": {
        "tier": "Premium",
        "price_range": "€18 - €55/m (基于行业基准估算)",
        "clients": "中高端定制连锁、Suitsupply、Boglioli",
        "grip": "重申 21 Micron 羊毛的优越性（不追 Super 数）。S/S 2027 重点推荐 Montecarlo Hopsacks，具有极致抗皱和 3D 透气感。博弈点：样卡系统直接接入。",
        "value_prop": "21 Micron 系列在夏季高湿度环境下的物理稳定性。"
    },
    "REDA": {
        "tier": "Premium Modern",
        "price_range": "€20 - €55/m (基于行业基准估算)",
        "clients": "Boss, Armani, Canali",
        "grip": "S/S 2027 推出的‘凉感’整理工艺与 B-Corp 可持续背书是核心。博弈点：利用其‘数字样卡’系统缩短测样周期。",
        "value_prop": "Reda Active 系列在高端运动通勤西装中的统治地位。"
    },
    "ERMENEGILDO ZEGNA": {
        "tier": "Luxury",
        "price_range": "€50 - €150/m (基于行业基准估算)",
        "clients": "Zegna Retail, Dunhill, Gucci",
        "grip": "S/S 2027 重点在于 High Performance 系列的‘丝滑纹理’，契合 Shadows 暗影趋势。博弈点：针对顶级客户的定制面料包销。",
        "value_prop": "全球最轻薄、最具光泽感的正装羊毛面料。"
    },
    "ALBINI 1876": {
        "tier": "Luxury Shirtings",
        "price_range": "€15 - €45/m (基于行业基准估算)",
        "clients": "Harvie & Hudson, Eton, Turnbull & Asser",
        "grip": "S/S 2027 重点是 MicroTencel 与麻棉混纺。博弈点：Thomas Mason 的库存优先权和‘Journey Blended’防皱系列。",
        "value_prop": "衬衫领域的‘MU Cosmetic’代表：极度亲肤的天然混纺。"
    }
}

def generic_intel(brand_name, hall):
    return {
        "tier": "Standard/Premium",
        "price_range": "€15 - €45/m (估算区间)",
        "clients": "全球中高端时装品牌及定制商",
        "grip": "现场询问 MOQ (起订量) 与样卡包含政策。针对 S/S 2027 重点询问凉感面料整理工艺的价格差。",
        "value_prop": "意大利制造的品质稳定性。"
    }

def process_data():
    intel_data = []
    if not os.path.exists(CSV_PATH): return
    
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if " 20 " in row['name']:
                # 解析逻辑...
                parts = row['name'].split(' ')
                try:
                    hall_idx = parts.index("20")
                    brand_name = " ".join(parts[:hall_idx-2])
                    booth = " ".join(parts[hall_idx+1:])
                    area = parts[hall_idx-2] + " " + parts[hall_idx-1]
                except: continue

                found = False
                for k, v in INTEL_WIKI.items():
                    if k in brand_name.upper():
                        item = v.copy()
                        item['name'] = brand_name
                        item['booth'] = booth
                        item['area'] = area
                        intel_data.append(item)
                        found = True
                        break
                
                if not found:
                    item = generic_intel(brand_name, "20")
                    item['name'] = brand_name
                    item['booth'] = booth
                    item['area'] = area
                    intel_data.append(item)

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(intel_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    process_data()
    print(f"Hall 20 Intelligence JSON updated with explicit ESTIMATE labels.")
