import os
import asyncio
from playwright.async_api import async_playwright

os.environ["NO_PROXY"] = "127.0.0.1,localhost"

async def run_search():
    async with async_playwright() as p:
        print("🚀 启动环境隔离浏览器 (DuckDuckGo)...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        query = "Milano Unica 42 Hall 20 Ideabiella Shirt Avenue details"
        print(f"🔍 搜索: {query}")
        
        # 使用 DuckDuckGo 绕过 Google CAPTCHA
        await page.goto(f"https://duckduckgo.com/?q={query.replace(' ', '+')}")
        await page.wait_for_timeout(4000)
        
        screenshot_path = os.path.abspath("ddg_search_result.png")
        await page.screenshot(path=screenshot_path)
        
        # 提取结果描述
        results = await page.query_selector_all("article")
        print("\n📝 DuckDuckGo 搜索摘要：")
        for i, res in enumerate(results[:5]):
            text = await res.inner_text()
            print(f"[{i+1}] {text[:200]}...")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_search())
