import os
import time
import requests
import pdfplumber
import pandas as pd
from playwright.sync_api import sync_playwright
from rich.console import Console
from rich.progress import Progress

# --- 环境隔离 (Environment Isolation) ---
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
os.environ["no_proxy"] = "127.0.0.1,localhost"

console = Console()

PDF_URL = "https://s3.eu-west-3.amazonaws.com/customer-it.milanounica.www/3317/6598/5115/Milano_Unica_42_Edizione_Elenco_Espositori.pdf"
WEB_URL = "https://e.milanounica.it/en/milanounica/fairs/milanounica42/exhibitors?mtm_campaign=eMU14&mtm_source=sitoweb&mtm_placement=espositori"

def extract_from_pdf(url):
    console.print(f"[bold blue]正在解析 PDF:[/bold blue] {url}")
    response = requests.get(url)
    with open("temp_exhibitors.pdf", "wb") as f:
        f.write(response.content)
    
    exhibitors = []
    with pdfplumber.open("temp_exhibitors.pdf") as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line in lines:
                    # 简单启发式抓取：假设每行可能包含展商名和展位号
                    # Milano Unica PDF 通常每行是：EXHIBITOR NAME | BOOTH
                    if "|" in line:
                        parts = line.split("|")
                        exhibitors.append({"name": parts[0].strip(), "booth": parts[1].strip(), "source": "PDF"})
                    elif len(line.strip()) > 3:
                        # 兜底处理
                        exhibitors.append({"name": line.strip(), "booth": "Unknown", "source": "PDF"})
    
    os.remove("temp_exhibitors.pdf")
    return exhibitors

def extract_from_web(url):
    console.print(f"[bold blue]正在解析 网页 (Lazy Loading):[/bold blue] {url}")
    exhibitors = []
    with sync_playwright() as p:
        # 强制不使用系统代理连接浏览器
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        # 处理可能的 Cookie 或 弹窗
        try:
            page.click("text=Accept", timeout=5000)
        except:
            pass

        # 懒加载：不断向下拉，直到不再加载新元素
        last_height = page.evaluate("document.body.scrollHeight")
        while True:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2) # 等待加载
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            console.print("  [dim]正在滚动加载更多展商...[/dim]")

        # 抓取展商卡片
        # 假设展商在某个具名类或结构中，Milano Unica 网页通常使用 list 结构
        items = page.query_selector_all(".exhibitor-item, .card-exhibitor, .mu-exhibitor") # 尝试常见选择器
        if not items:
            # 如果没找到，抓取所有文本块分析
            # 这里使用更通用的选择器，实际可能需要根据 DOM 调整
            items = page.query_selector_all("div[class*='exhibitor']") 

        for item in items:
            name = item.inner_text().split('\n')[0].strip()
            # 展位号通常在特定 span 或 div 中
            booth = "Unknown"
            try:
                booth_elem = item.query_selector("span[class*='booth'], div[class*='hall']")
                if booth_elem:
                    booth = booth_elem.inner_text().strip()
            except:
                pass
            
            if name:
                exhibitors.append({"name": name, "booth": booth, "source": "WEB"})
        
        browser.close()
    return exhibitors

def main():
    with Progress() as progress:
        task1 = progress.add_task("[cyan]任务执行中...", total=2)
        
        # 抓取数据
        all_data = []
        try:
            pdf_data = extract_from_pdf(PDF_URL)
            all_data.extend(pdf_data)
        except Exception as e:
            console.print(f"[red]PDF 抓取失败: {e}[/red]")
        progress.update(task1, advance=1)
        
        try:
            web_data = extract_from_web(WEB_URL)
            all_data.extend(web_data)
        except Exception as e:
            console.print(f"[red]网页抓取失败: {e}[/red]")
        progress.update(task1, advance=1)

    # 汇总并保存
    df = pd.DataFrame(all_data).drop_duplicates(subset=['name'])
    
    # 生成 Markdown
    markdown_content = "# Milano Unica 42 Exhibitor List (Draft)\n\n"
    markdown_content += f"**Total Unique Exhibitors:** {len(df)}\n\n"
    markdown_content += "| Name | Booth | Source |\n| --- | --- | --- |\n"
    for _, row in df.iterrows():
        markdown_content += f"| {row['name']} | {row['booth']} | {row['source']} |\n"
    
    with open("EXHIBITOR_LIST.md", "w") as f:
        f.write(markdown_content)
    
    console.print(f"\n[bold green]✅ 抓取完成！已生成 EXHIBITOR_LIST.md (共 {len(df)} 家展商)[/bold green]")

if __name__ == "__main__":
    main()
