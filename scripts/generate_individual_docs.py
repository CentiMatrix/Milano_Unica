import pandas as pd
import os
import re

# --- 环境隔离 ---
os.environ["NO_PROXY"] = "127.0.0.1,localhost"

TARGET_DIR = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/Milano_Unica"
INPUT_MD = "EXHIBITOR_LIST.md"

def slugify(text):
    # 将名称转换为合法的文件名
    text = re.sub(r'[^\w\s-]', '', text).strip().replace(' ', '_')
    return text[:50] # 限制长度

def main():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    # 读取清洗后的数据
    # 由于之前导出的是 CSV 也有 MD，我们直接从 MD 解析回来的 Table 读可能有点烦，
    # 幸好我们有精简后的逻辑，或者直接重跑一次逻辑。
    # 这里我们演示通过正则表达式解析 EXHIBITOR_LIST.md
    
    with open(INPUT_MD, "r") as f:
        content = f.read()

    # 匹配表格行 | Name | Area | Hall | Stand |
    pattern = r'\| (.*?) \| (.*?) \| (.*?) \| (.*?) \|'
    matches = re.findall(pattern, content)
    
    # 跳过 Header 和 分隔线
    exhibitors = matches[2:] 

    for name, area, hall, stand in exhibitors:
        name = name.strip()
        filename = f"{slugify(name)}.md"
        filepath = os.path.join(TARGET_DIR, filename)
        
        md_content = f"""# {name}

## 📍 展位信息 (Location)
- **展区 (Area)**: {area.strip()}
- **展馆 (Hall)**: {hall.strip()}
- **展位 (Stand)**: {stand.strip()}

## 🔍 商户概况 (Exhibitor Profile)
- [ ] 品牌背景调研
- [ ] 产品特色分析
- [ ] 历史采购记录

## 📋 采购备注 (Purchasing Notes)
- 
"""
        with open(filepath, "w") as f:
            f.write(md_content)

    print(f"Generated {len(exhibitors)} files in {TARGET_DIR}")

if __name__ == "__main__":
    main()
