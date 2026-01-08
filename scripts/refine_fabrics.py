import os
import shutil
import re

# --- 环境隔离 ---
os.environ["NO_PROXY"] = "127.0.0.1,localhost"

INPUT_CSV = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/pdf_exhibitors.csv"
BASE_DIR = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/Milano_Unica/Moda In Fabrics"

def slugify(text):
    text = re.sub(r'[^\w\s-]', '', text).strip().replace(' ', '_')
    return text[:50]

# 解析逻辑
def parse_line_refined(line):
    # 匹配细作品类
    match = re.search(r'(.*?)\s+(Moda In Fabrics (Cotton Woolly|Knit|Silky Print|Tecno|Lace&Embroidery))\s+(\d+)\s+([A-Z]\d+)', line)
    if match:
        return {
            "Name": match.group(1).strip(),
            "SubCategory": match.group(3).strip(),
            "Hall": match.group(4).strip(),
            "Stand": match.group(5).strip()
        }
    return None

def main():
    import pandas as pd
    df_raw = pd.read_csv(INPUT_CSV)
    
    stats = {}

    for _, row in df_raw.iterrows():
        line = str(row['name'])
        parsed = parse_line_refined(line)
        if parsed:
            subcat = parsed['SubCategory'].replace('&', ' & ')
            target_subdir = os.path.join(BASE_DIR, subcat)
            
            if not os.path.exists(target_subdir):
                os.makedirs(target_subdir)

            filename = f"{slugify(parsed['Name'])}.md"
            src_path = os.path.join(BASE_DIR, filename)
            dst_path = os.path.join(target_subdir, filename)

            if os.path.exists(src_path):
                shutil.move(src_path, dst_path)
                stats[subcat] = stats.get(subcat, 0) + 1
            elif os.path.exists(dst_path):
                stats[subcat] = stats.get(subcat, 0) + 1

    print("Sub-categorization within Moda In Fabrics complete:")
    for cat, count in stats.items():
        print(f" - {cat}: {count} files")

if __name__ == "__main__":
    main()
