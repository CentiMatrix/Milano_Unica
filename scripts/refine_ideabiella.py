import os
import shutil
import re

# --- 环境隔离 ---
os.environ["NO_PROXY"] = "127.0.0.1,localhost"

BASE_DIR = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/Milano_Unica/Ideabiella"

# 映射分类
CATEGORIES = {
    "Global Icons": [
        "LORO_PIANA", "VITALE_BARBERIS_CANONICO", "REDA", "ERMENEGILDO_ZEGNA", 
        "PIACENZA", "DRAGO", "TRABALDO_TOGNA", "LANIFICIO_CARLO_BARBERA", "LANIFICIO_LUIGI_COLOMBO"
    ],
    "British & Northern Heritage": [
        "HARRIS_TWEED", "MOON", "JOSHUA_ELLIS", "ALFRED_BROWN", "BOWER_ROEBUCK", 
        "JOHN_FOSTER", "SAVILE_CLIFFORD", "WILLIAM_HALSTEAD", "KYNOCH", "MALLALIEUS",
        "MARLING_&_EVANS", "JOSEPH_H_CLISSOLD", "FERNMOOR", "MAGEE_WEAVING"
    ],
    "Creative & Specialists": [
        "PONTOGLIO", "SOLBIATI", "BONOTTO", "FALIERO_SARTI", "DUCA_VISCONTI", 
        "VISCONTI_DI_MODRONE", "EGO", "PECCI", "TESJ", "RATTI", "CARNET", 
        "MARIELLE", "NALYA", "REGGIANI", "STEPHEN_WALTERS", "TBM"
    ],
    "Biella Sartorial Excellence": [] # 默认分类
}

def get_category(filename):
    name_upper = filename.upper()
    for cat, brands in CATEGORIES.items():
        for brand in brands:
            if brand in name_upper:
                return cat
    return "Biella Sartorial Excellence"

def main():
    if not os.path.exists(BASE_DIR):
        return

    # 先创建目录
    for cat in CATEGORIES.keys():
        cat_path = os.path.join(BASE_DIR, cat)
        if not os.path.exists(cat_path):
            os.makedirs(cat_path)

    # 移动文件
    files = [f for f in os.listdir(BASE_DIR) if f.endswith('.md') and f != '1 roadmap.md']
    stats = {}

    for f_name in files:
        # 跳过已经是在子目录里的
        if os.path.isdir(os.path.join(BASE_DIR, f_name)):
            continue
            
        cat = get_category(f_name)
        src = os.path.join(BASE_DIR, f_name)
        dst = os.path.join(BASE_DIR, cat, f_name)
        
        shutil.move(src, dst)
        stats[cat] = stats.get(cat, 0) + 1

    print("Ideabiella Categorization complete:")
    for cat, count in stats.items():
        print(f" - {cat}: {count} files")

if __name__ == "__main__":
    main()
