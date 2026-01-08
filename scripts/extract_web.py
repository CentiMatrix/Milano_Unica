import os
import time
import pandas as pd
from playwright.sync_api import sync_playwright
from rich.console import Console

os.environ["NO_PROXY"] = "127.0.0.1,localhost"
console = Console()

url = "https://e.milanounica.it/en/milanounica/fairs/milanounica42/exhibitors"

def main():
    try:
        console.print(f"[bold blue]Step 1: Launching Browser...[/bold blue]")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            console.print(f"[bold blue]Step 2: Loading Webpage...[/bold blue]")
            page.goto(url, wait_until="networkidle", timeout=60000)
            
            # 懒加载处理
            console.print(f"[bold blue]Step 3: Scrolling for lazy-loaded content...[/bold blue]")
            for i in range(5): # 初始滚动5次尝试
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(3)
                console.print(f"  Scroll {i+1}...")
            
            # 抓取数据
            console.print(f"[bold blue]Step 4: Extracting data...[/bold blue]")
            # 尝试根据 MU 网页结构提取
            # 展商通常在 .exhibitor-card 或类似结构中
            cards = page.query_selector_all("a.card-exhibitor, .exhibitor-item")
            if not cards:
                # 备选方案：抓取所有链接文本
                cards = page.query_selector_all("a")
            
            exhibitors = []
            for card in cards:
                text = card.inner_text().strip()
                if text and len(text) > 2:
                    exhibitors.append({"name": text.split('\n')[0], "info": text.replace('\n', ' | ')})
            
            df = pd.DataFrame(exhibitors)
            df.to_csv("web_exhibitors.csv", index=False)
            console.print(f"[green]Web Extraction Success: {len(df)} potential items found.[/green]")
            browser.close()
    except Exception as e:
        console.print(f"[red]Web Error: {e}[/red]")

if __name__ == "__main__":
    main()
