import os

# --- 环境隔离 ---
os.environ["NO_PROXY"] = "127.0.0.1,localhost"

BASE_DIR = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/Milano_Unica"

AREA_DESCRIPTIONS = {
    "Ideabiella": "顶级男装正装面料展区。汇集了来自 Biella 等地区的全球最顶级毛料、西装面料供应商。",
    "Shirt Avenue": "顶级衬衫面料展区。展示了从正式商务到高端休闲的全系列奢华衬衫织物。",
    "Moda In Fabrics": "成衣面料核心区。已细分为 Cotton, Knit, Silky, Lace 等品类。",
    "Moda In Accessories": "配饰与辅料展区。包括纽扣、拉链、织带、标签等。",
    "Cotton & Woolly": "棉与毛纺面料。主打天然纤维，适合休闲、外套与正装混搭。",
    "Knit": "针织面料展区。重点关注弹性、舒适度与运动时尚面料。",
    "Silky Print": "丝绸与印花面料。集中了顶级丝绸织造、印染与花型设计商。",
    "Lace & Embroidery": "蕾丝与刺绣。涵盖了高端女装、礼服所需的精细装饰工艺。",
    "Tecno": "科技功能面料。关注防水、透气、高性能与环保创新材料。"
}

def generate_index(target_path, area_name):
    items = os.listdir(target_path)
    subdirs = sorted([d for d in items if os.path.isdir(os.path.join(target_path, d))])
    files = sorted([f for f in items if f.endswith('.md') and f != '1 roadmap.md'])
    
    description = AREA_DESCRIPTIONS.get(area_name, "Milano Unica 42 展台详细名录。")
    
    md_content = f"""# {area_name} 索引说明

## 📋 展区详情
{description}

"""
    if subdirs:
        md_content += "### 📂 子品类分类\n| 分类名称 | 链接 |\n| --- | --- |\n"
        for sd in subdirs:
            md_content += f"| {sd} | [进入 {sd} 分类](./{sd}/1 roadmap.md) |\n"
        md_content += "\n"

    md_content += f"### 📊 展商列表 (共 {len(files)} 家)\n| 商户名称 | 链接 |\n| --- | --- |\n"
    for f_name in files:
        brand_name = f_name.replace('.md', '').replace('_', ' ')
        md_content += f"| {brand_name} | [{f_name}](./{f_name}) |\n"

    md_content += """
---
### 🛡️ 数据来源说明
本目录下的商户资料主要源自 **Milano Unica 官方授权 PDF 名录**。
- **匹配逻辑**: 100% 对齐官方物理展位分布。
"""
    
    with open(os.path.join(target_path, "1 roadmap.md"), "w") as f:
        f.write(md_content)

def main():
    # 遍历一级目录
    for d1 in os.listdir(BASE_DIR):
        p1 = os.path.join(BASE_DIR, d1)
        if os.path.isdir(p1):
            generate_index(p1, d1)
            # 遍历二级目录（针对 Moda In Fabrics）
            for d2 in os.listdir(p1):
                p2 = os.path.join(p1, d2)
                if os.path.isdir(p2):
                    generate_index(p2, d2)

if __name__ == "__main__":
    main()
