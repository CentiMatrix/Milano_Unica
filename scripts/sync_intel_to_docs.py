import os
import json

# --- 环境隔离 ---
os.environ["NO_PROXY"] = "127.0.0.1,localhost"

INTEL_JSON = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/hall20_intel.json"
ROOT_DIR = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/Milano_Unica"

def sync_intel():
    with open(INTEL_JSON, 'r', encoding='utf-8') as f:
        intel_list = json.load(f)
    
    intel_map = {item['name'].upper(): item for item in intel_list}
    
    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        for f in files:
            if f.endswith('.md') and f != '1 roadmap.md':
                path = os.path.join(root, f)
                # 模糊匹配名称
                brand_key = f.replace('.md', '').replace('_', ' ').upper()
                
                matched_intel = None
                for k, v in intel_map.items():
                    if k in brand_key or brand_key in k:
                        matched_intel = v
                        break
                
                if matched_intel:
                    with open(path, 'r', encoding='utf-8') as file:
                        content = file.read()
                    
                    # 构造新内容
                    new_section = (
                        "\n## 💰 商业决策情报 (Commercial Intelligence - 行业基准估算)\n"
                        f"> [!NOTE]\n"
                        f"> 展会 S/S 2027 批发价受量级影响且属于商业机密，下述价格为基于‘定制单剪 (Cut-length)’市场行情的基准估算，仅供采购预算梯度参考。\n\n"
                        f"- **市场档位 (Tier)**: {matched_intel['tier']}\n"
                        f"- **价格区间 (Price)**: {matched_intel['price_range']}\n"
                        f"- **核心服务客户**: {matched_intel['clients']}\n"
                        f"- **核心价值 (Value)**: {matched_intel['value_prop']}\n\n"
                        "### 📥 博弈点与利益互通 (Strategic Grip)\n"
                        f"> {matched_intel['grip']}\n"
                    )
                    
                    # 如果已存在，则替换；如果不存在，则追加
                    if "## 💰 商业决策情报" in content:
                        # 简单的正则或查找替换逻辑备份：这里采用简单的切片替换，确保最新
                        base_content = content.split("## 💰 商业决策情报")[0]
                        updated_content = base_content + new_section
                    else:
                        updated_content = content + "\n" + new_section
                    
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(updated_content)
                    count += 1

    print(f"Synced commercial intelligence to {count} brand documents.")

if __name__ == "__main__":
    sync_intel()
