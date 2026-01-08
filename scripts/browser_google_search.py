import os
import asyncio
from playwright.async_api import async_playwright

# 🛑 关键：通过 NO_PROXY 解决 CDP 400 错误
os.environ["NO_PROXY"] = "127.0.0.1,localhost"

async def run_search():
    async with async_playwright() as p:
        print("🚀 正在启动环境隔离浏览器...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        query = "Milano Unica 42 Ideabiella Hall 20 exhibitors list and floor plan"
        print(f"🔍 正在搜索: {query}")
        
        await page.goto(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        await page.wait_for_timeout(3000) # 等待加载
        
        # 截图保存结果
        screenshot_path = os.path.abspath("google_search_result.png")
        await page.screenshot(path=screenshot_path)
        print(f"📸 搜索结果截图已保存: {screenshot_path}")
        
        # 提取前 5 个结果标题
        results = await page.query_selector_all("h3")
        print("\n📝 搜索结果前五条：")
        for i, res in enumerate(results[:5]):
            title = await res.inner_text()
            print(f"{i+1}. {title}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_search())
