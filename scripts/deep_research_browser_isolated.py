import os
import asyncio
from playwright.async_api import async_playwright

# --- 环境隔离：绕过代理导致的 CDP 400 错误 ---
os.environ["NO_PROXY"] = "127.0.0.1,localhost"

async def research_hall20():
    async with async_playwright() as p:
        # 启动浏览器，明确连接到本地端口时绕过代理
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Searching for MU42 Hall 20 Floor Plan...")
        await page.goto("https://www.google.com/search?q=Milano+Unica+42+Hall+20+floor+plan+booth+map")
        await page.wait_for_timeout(2000)
        await page.screenshot(path="mu42_search_results.png")
        
        # 尝试寻找官方 PDF 或 交互式地图链接
        links = await page.query_selector_all("a")
        found_map = False
        for link in links:
            href = await link.get_attribute("href")
            if href and "milanounica.it" in href and "map" in href.lower():
                print(f"Found potential map link: {href}")
                found_map = True
                break
        
        if not found_map:
            print("No direct map link found on first page. Saving screenshot of search.")

        # 深入调研几个核心品牌的价格政策
        brands = ["Loro Piana", "Vitale Barberis Canonico", "Albini 1876"]
        for brand in brands:
            print(f"Researching commercial details for {brand}...")
            await page.goto(f"https://www.google.com/search?q={brand.replace(' ', '+')}+fabric+wholesale+price+bespoke+clients")
            await page.wait_for_timeout(2000)
            # 获取第一页的前几个摘要
            results = await page.query_selector_all("div.g")
            summary = ""
            for i, res in enumerate(results[:3]):
                text = await res.inner_text()
                summary += f"\nResult {i+1}: {text[:300]}..."
            
            with open(f"{brand.replace(' ', '_')}_intel.txt", "w", encoding="utf-8") as f:
                f.write(summary)

        await browser.close()
        print("Research complete. Intel files and screenshot saved.")

if __name__ == "__main__":
    asyncio.run(research_hall20())
