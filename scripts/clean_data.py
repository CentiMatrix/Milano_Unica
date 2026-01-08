import pandas as pd
import re

def clean_name(name):
    # 移除页码、日期等非展商信息
    ignore_patterns = [
        r'ELENCO ESPOSITORI', r'LIST OF EXHIBITORS', r'MILANO UNICA',
        r'Primavera/Estate', r'gennaio/January', r'milanounica.it',
        r'HALL STAND', r'Aree Espositive', r'Ordine alfabetico'
    ]
    for p in ignore_patterns:
        if re.search(p, name, re.I):
            return None
    return name.strip()

def parse_line(line):
    # 典型格式: BRAND NAME Area Hall Stand
    # 例如: 18 STORE Moda In Fabrics 16 B50
    # 尝试匹配最后的 Hall (数字) 和 Stand (字母+数字)
    match = re.search(r'(.*?)\s+(Ideabiella|Moda In.*|Shirt Avenue|Japan Observatory|Korea Observatory|Innovation Area|MarediModa|MU Designers|MU Vintage|MU Info & Style|MU Trade Press|MU Special Contents)\s+(\d+)\s+([A-Z]\d+)', line)
    if match:
        return {
            "Name": match.group(1).strip(),
            "Area": match.group(2).strip(),
            "Hall": match.group(3).strip(),
            "Stand": match.group(4).strip()
        }
    return None

def main():
    df_raw = pd.read_csv("pdf_exhibitors.csv")
    cleaned_data = []
    
    for _, row in df_raw.iterrows():
        line = str(row['name'])
        parsed = parse_line(line)
        if parsed:
            cleaned_data.append(parsed)
        else:
            # 如果正则匹配失败，尝试简单清洗
            name = clean_name(line)
            if name and len(name) > 3:
                # 尝试分割最后两个词作为 Hall 和 Stand
                parts = name.split()
                if len(parts) >= 3:
                    stand = parts[-1]
                    hall = parts[-2]
                    if re.match(r'[A-Z]\d+', stand) and hall.isdigit():
                        cleaned_data.append({
                            "Name": " ".join(parts[:-3]),
                            "Area": parts[-3],
                            "Hall": hall,
                            "Stand": stand
                        })
    
    df = pd.DataFrame(cleaned_data).drop_duplicates()
    
    # 排序：先 Hall 再 Stand
    df['HallNum'] = pd.to_numeric(df['Hall'], errors='coerce')
    df = df.sort_values(by=['HallNum', 'Stand'])
    
    # 生成 Markdown
    md = "# Milano Unica 42 展商名录 (精简版)\n\n"
    md += f"**收录展商总数:** {len(df)}\n\n"
    md += "| 展商名称 (Name) | 展区 (Area) | 展馆 (Hall) | 展位 (Stand) |\n"
    md += "| --- | --- | --- | --- |\n"
    for _, row in df.iterrows():
        md += f"| {row['Name']} | {row['Area']} | {row['Hall']} | {row['Stand']} |\n"
    
    with open("EXHIBITOR_LIST.md", "w") as f:
        f.write(md)
    
    print(f"Cleanup done. {len(df)} exhibitors saved to EXHIBITOR_LIST.md")

if __name__ == "__main__":
    main()
