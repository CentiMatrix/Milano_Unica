import os
import shutil
import re

# --- 环境隔离 ---
os.environ["NO_PROXY"] = "127.0.0.1,localhost"

BASE_DIR = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/Milano_Unica"
INPUT_MD = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/EXHIBITOR_LIST.md"

def slugify(text):
    text = re.sub(r'[^\w\s-]', '', text).strip().replace(' ', '_')
    return text[:50]

def main():
    if not os.path.exists(BASE_DIR):
        print(f"Directory {BASE_DIR} does not exist.")
        return

    with open(INPUT_MD, "r") as f:
        content = f.read()

    # 匹配表格行 | Name | Area | Hall | Stand |
    pattern = r'\| (.*?) \| (.*?) \| (.*?) \| (.*?) \|'
    matches = re.findall(pattern, content)
    
    # 跳过 Header 和 分隔线
    exhibitors = matches[2:] 

    stats = {}

    for name_raw, area_raw, hall, stand in exhibitors:
        name = name_raw.strip()
        area = area_raw.strip()
        
        # 处理特殊 Area 名称（移除斜杠等非法路径字符）
        area_folder = area.replace('/', '&').replace('\\', '&').strip()
        if not area_folder:
            area_folder = "Other"
            
        target_subdir = os.path.join(BASE_DIR, area_folder)
        if not os.path.exists(target_subdir):
            os.makedirs(target_subdir)

        filename = f"{slugify(name)}.md"
        src_path = os.path.join(BASE_DIR, filename)
        dst_path = os.path.join(target_subdir, filename)

        if os.path.exists(src_path):
            shutil.move(src_path, dst_path)
            stats[area_folder] = stats.get(area_folder, 0) + 1
        else:
            # 检查是否已经在目标目录
            if os.path.exists(dst_path):
                stats[area_folder] = stats.get(area_folder, 0) + 1

    print("Categorization complete:")
    for area, count in stats.items():
        print(f" - {area}: {count} files")

if __name__ == "__main__":
    main()
