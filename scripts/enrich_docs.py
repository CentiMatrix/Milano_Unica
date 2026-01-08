import os

# --- 环境隔离 ---
os.environ["NO_PROXY"] = "127.0.0.1,localhost"

ROOT_DIR = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/Milano_Unica"

# S/S 2027 Trend Data
TRENDS_2027 = """
## 🌟 S/S 2027 趋势分析: "MU Cosmetic" (纺织品与化妆品的交织)
本季核心理念是“身体体验”与材料的融合，分为三大子主题：
- **Natural (自然)**: 有机棉、水洗亚麻、竹纤维。色调：绿茶色、大地裸色、天蓝色。强调“亲肤”感。
- **Shadows (暗影)**: 烟灰、烟熏银、勃艮第红绸。色调：粉末玫瑰、暗珠色。适合高级正装的“优雅光影”。
- **Sun (阳光)**: 透气性、凉感、防晒。色调：芦荟绿、海蓝、亮橙。适合高功能性轻薄夏季西装。
"""

BRAND_INFO = {
    "LORO PIANA": "全球奢侈面料天花板。西装主理人必看项目。S/S 2027 重点：极轻量羊绒与丝绸混纺 (Sunset 系列)，以及 Linen Denim 的深度应用。",
    "VITALE BARBERIS CANONICO": "拥有 350 年历史的 Biella 巨头。定制店的基石供应商。重点：21 Micron 强捻混纺，针对夏季的透气性和抗皱性。",
    "REDA": "现代数字纺织领军者，全产业链可持续。重点：Reda Active 高性能美利奴羊毛，针对 S/S 2027 提供‘凉感’整理工艺。",
    "ERMENEGILDO ZEGNA": "顶级奢华与创意的代名词。重点：High Performance 系列，本季强调‘丝滑纹理’，完美契合 Shadows 趋势。",
    "ALBINI": "衬衫面料全球标准。包含 Thomas Mason。重点：海岛棉与亚麻混纺，契合 Natural 主题中的‘亲肤感’。",
    "SOLBIATI": "亚麻之王。重点：针对西装主理人，其 S/S 2027 提供了更高比例的文件纹理亚麻，以及亮粉色 (Glossy Pink) 的点缀。",
    "DRAGO": "高支数羊毛专家。重点：Super 130s - 160s 的超轻薄夏季正装面料，契合 Sun 主题的防晒与透气需求。"
}

def update_docs():
    for root, dirs, files in os.walk(ROOT_DIR):
        for f in files:
            if f.endswith('.md') and f != '1 roadmap.md':
                path = os.path.join(root, f)
                brand_name = f.replace('.md', '').replace('_', ' ').upper()
                
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Check if already updated
                if "S/S 2027 趋势分析" in content:
                    continue
                
                # Build enrichment
                enrichment = "\n" + TRENDS_2027
                
                # Specific brand info
                found_brand = False
                for b_name, b_info in BRAND_INFO.items():
                    if b_name in brand_name:
                        enrichment += f"\n## 💼 商业情报与产品建议\n{b_info}\n"
                        found_brand = True
                        break
                
                if not found_brand:
                    enrichment += "\n## 💼 商业情报\n通用趋势：本季该品牌预计将针对 'MU Cosmetic' 主题推出更具亲肤感和物理凉感的夏季混纺面料。\n"
                
                # Append to file
                with open(path, 'a', encoding='utf-8') as file:
                    file.write(enrichment)

if __name__ == "__main__":
    update_docs()
    print("Individual docs updated with S/S 2027 trends and commercial info.")
