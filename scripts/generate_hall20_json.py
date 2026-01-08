import os
import json
import csv

# --- 环境隔离 ---
os.environ["NO_PROXY"] = "127.0.0.1,localhost"

CSV_PATH = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/pdf_exhibitors.csv"
OUTPUT_JSON = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/hall20_intel.json"

# 行业知识库快照 (针对 Hall 20 核心品牌)
INTEL_WIKI = {
    # Ideabiella - Global Icons
    "LORO PIANA": {
        "tier": "Luxury+",
        "price_range": "€80 - €300+/m",
        "clients": "Brioni, Kiton, Tom Ford, Zegna",
        "grip": "定制配额极难拿。博弈点：样卡费用减免，利用其品牌溢价说服终端客户接受 2-3 月货期。",
        "value_prop": "全球公认的面料天花板，特别是羊绒与极轻毛料 (Wish, Australis)。"
    },
    "VITALE BARBERIS CANONICO": {
        "tier": "Premium Heritage",
        "price_range": "€18 - €60/m",
        "clients": "Brooks Brothers, Hackett, Suitsupply, Boglioli",
        "grip": "产量大，现货充足。博弈点：MOQ 谈库位保留，西装主理人可尝试谈其定制系统的直接 API 接入。",
        "value_prop": "定制店的利润基石，21 Micron 系列是抗皱神器。"
    },
    "REDA": {
        "tier": "Premium Modern",
        "price_range": "€20 - €55/m",
        "clients": "Boss, Armani, Canali",
        "grip": "数字化程度极高。博弈点：可持续证书支持 (B-Corp)，适合作为品牌 ESG 营销素材。",
        "value_prop": "Reda Active 是目前最好的运动西装面料。"
    },
    "ERMENEGILDO ZEGNA": {
        "tier": "Luxury",
        "price_range": "€50 - €150/m",
        "clients": "Zegna Retail, Dunhill, Gucci",
        "grip": "高端定制线非常强势。博弈点：全品类合作谈判 (从面料到辅料) 以获取更优返点。",
        "value_prop": "15 Milmil 15 等超精细面料的标杆。"
    },
    # Shirt Avenue
    "ALBINI 1876": {
        "tier": "Luxury Shirtings",
        "price_range": "€15 - €45/m",
        "clients": "Harvie & Hudson, Eton, Turnbull & Asser",
        "grip": "拥有 Thomas Mason。博弈点：利用其库存系统快速补货，减少库存压力。",
        "value_prop": "海岛棉与亚麻混纺的技术垄断者。"
    },
    "ALUMO": {
        "tier": "Ultra-Luxury Shirtings",
        "price_range": "€30 - €100+/m",
        "clients": "Hermes, Charvet, Stefano Ricci",
        "grip": "瑞士工匠。博弈点：针对极致定制客户，利用其‘原产地证明’作为溢价工具。",
        "value_prop": "200/2 甚至更高支数的代名词。"
    }
}

# 通用行业分层映射逻辑
def generic_intel(brand_name, hall):
    if "IDEABIELLA" in brand_name.upper() or hall == "20":
        return {
            "tier": "Premium Standard",
            "price_range": "€15 - €40/m",
            "clients": "高端成衣品牌与全球中大型定制零售商",
            "grip": "关注初次起订量 (MOQ) 优惠，样卡返还政策。",
            "value_prop": "Biella 产区稳定质量保障。"
        }
    return {
        "tier": "Standard",
        "price_range": "€10 - €25/m",
        "clients": "快时尚及大众精品品牌",
        "grip": "价格敏感，批量折扣大。",
        "value_prop": "性价比高。"
    }

def process_data():
    intel_data = []
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 只取 Hall 20
            if " 20 " in row['name']:
                # 解析名称和摊位
                parts = row['name'].split(' ')
                # 这里逻辑需要精细化，因为 CSV 里的格式是 "ALBIATE 1830 Shirt Avenue 20 A01"
                # 我们寻找最后一个数字 (20) 之后的是摊位号
                try:
                    hall_idx = parts.index("20")
                    brand_name = " ".join(parts[:hall_idx-2]) # 排除 Area 名称
                    booth = " ".join(parts[hall_idx+1:])
                    area = parts[hall_idx-2] + " " + parts[hall_idx-1]
                except:
                    brand_name = row['name']
                    booth = "TBD"
                    area = "Hall 20"

                # 匹配情报
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
    print(f"Hall 20 Intelligence JSON generated at {OUTPUT_JSON}")
