import os
import shutil
import pandas as pd
import re

# --- 环境隔离 ---
os.environ["NO_PROXY"] = "127.0.0.1,localhost"

INPUT_MD = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/EXHIBITOR_LIST.md"
BASE_DIR = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/Milano_Unica/Moda In Fabrics"

def slugify(text):
    text = re.sub(r'[^\w\s-]', '', text).strip().replace(' ', '_')
    return text[:50]

def categorize(name, hall):
    name_upper = name.upper()
    hall = str(hall).strip()
    
    # 优先根据 Hall 判断大致方向
    # Hall 12 -> Silky / Lace
    # Hall 16 -> Cotton / Knit / Tecno
    
    if hall == "12":
        if any(w in name_upper for w in ["LACE", "EMBROIDERY", "RICAMIFICIO", "DENTELLE", "TULLE"]):
            return "Lace & Embroidery"
        return "Silky Print"
    
    if hall == "16":
        if any(w in name_upper for w in ["JERSEY", "KNIT", "MAGLIFICIO", "MAGLIA", "PUNTO"]):
            return "Knit"
        if any(w in name_upper for w in ["TECNO", "PERFORMANCE", "CONVERTER", "WATERPROOF", "PROTECTION"]):
            return "Tecno"
        return "Cotton & Woolly"
    
    return "Others"

def main():
    with open(INPUT_MD, "r") as f:
        content = f.read()

    pattern = r'\| (.*?) \| (.*?) \| (.*?) \| (.*?) \|'
    matches = re.findall(pattern, content)
    
    exhibitors = matches[2:] 

    stats = {}

    for name_raw, area_raw, hall_raw, stand in exhibitors:
        name = name_raw.strip()
        area = area_raw.strip()
        hall = hall_raw.strip()
        
        if area == "Moda In Fabrics":
            subcat = categorize(name, hall)
            target_subdir = os.path.join(BASE_DIR, subcat)
            
            if not os.path.exists(target_subdir):
                os.makedirs(target_subdir)

            filename = f"{slugify(name)}.md"
            # 检查文件是否已经在根目录或在此目录
            src_path = os.path.join(BASE_DIR, filename)
            dst_path = os.path.join(target_subdir, filename)

            if os.path.exists(src_path):
                shutil.move(src_path, dst_path)
                stats[subcat] = stats.get(subcat, 0) + 1
            elif os.path.exists(dst_path):
                stats[subcat] = stats.get(subcat, 0) + 1

    print("Granular categorization complete:")
    for cat, count in stats.items():
        print(f" - {cat}: {count} files")

if __name__ == "__main__":
    main()
