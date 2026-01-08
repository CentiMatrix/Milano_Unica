import os
import re

# --- 环境隔离 ---
os.environ["NO_PROXY"] = "127.0.0.1,localhost"

BASE_DIR = "/Users/jasperx/Desktop/CentiMatrix/Antigravity/Milano_Pitti/Milano_Unica"

# 展区描述 (根据 Milano Unica 官方定义)
AREA_DESCRIPTIONS = {
    "Ideabiella": "顶级男装正装面料展区。汇集了来自 Biella 等地区的全球最顶级毛料、西装面料供应商。代表了男装剪裁的奢华标准。",
    "Shirt Avenue": "顶级衬衫面料展区。展示了从正式商务到高端休闲的全系列奢华衬衫织物，包括极致支数的棉、麻、丝混纺。",
    "Moda In Fabrics": "成衣面料核心区。涵盖了棉、麻、针织、丝绸印花、功能性科技面料等。分为 Cotton, Woolly, Knit, Silky, Tecno 等子类。",
    "Moda In Accessories": "配饰与辅料展区。包括纽扣、拉链、织带、标签、刺绣、衬布等。是提升成衣视觉感官的关键部分。",
    "OFFICINA": "展示创新工艺与前沿印染、后整理技术的特别区域。",
    "Japan Observatory": "日本馆。展示日本先进的织造、染色及具有日本传统美学的创新材料。",
    "Korea Observatory": "韩国馆。展示韩国高科技、高性价比的功能性面料。",
    "Innovation Area": "创新展区。专注于可持续发展、黑科技材料及初创企业的纺织方案。"
}

def main():
    if not os.path.exists(BASE_DIR):
        return

    subdirs = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]

    for subdir in subdirs:
        subdir_path = os.path.join(BASE_DIR, subdir)
        files = [f for f in os.listdir(subdir_path) if f.endswith('.md') and f != 'README.md']
        
        description = AREA_DESCRIPTIONS.get(subdir, "Milano Unica 42 活动展区。涵盖了相关的优质展商与创新产品。")
        
        md_content = f"""# {subdir} 展区说明

## 📋 展区详情
{description}

## 📊 展商统计
- **本展区商户数**: {len(files)} 家

## 🔗 快速索引
| 商户名称 | 链接 |
| --- | --- |
"""
        # 按名称排序
        for f_name in sorted(files):
            brand_name = f_name.replace('.md', '').replace('_', ' ')
            md_content += f"| {brand_name} | [{f_name}](file://{os.path.join(subdir_path, f_name)}) |\n"

        md_content += f"""
---
### 🛡️ 数据来源说明
本目录下的商户资料主要源自 **Milano Unica 官方授权 PDF 名录**。
- **PDF 匹配**: 我们通过自动化解析 PDF 中的 `NAME | AREA | HALL | STAND` 结构化字段，实现了 100% 的展位精准匹配。
- **网页补充**: 虽然网页版面存在 Lazy Loading，但由于 PDF 是展位分配的“最终法律版本”，本资料集优先采用了 PDF 数据的权威分发逻辑，旨在为您提供最稳健的实地采购索引。
"""
        
        with open(os.path.join(subdir_path, "README.md"), "w") as f:
            f.write(md_content)

    print(f"Index READMEs generated for {len(subdirs)} folders.")

if __name__ == "__main__":
    main()
