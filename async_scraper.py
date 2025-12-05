import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time
import argparse
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}

async def fetch(session, url, sem):
    async with sem:
        async with session.get(url) as r:
            r.raise_for_status()
            return await r.text()

def parse(html):
    soup = BeautifulSoup(html, "lxml")
    names = []
    total = 0.0
    for card in soup.select(".product-item, .catalog-item, .product-card"):
        t = card.select_one(".product-title, .product-name, .item-title")
        p = card.select_one(".price, .product-price, .item-price")
        if t:
            names.append(t.get_text(strip=True))
        if p:
            import re
            digits = re.sub(r"[^\d.]", "", p.get_text(" ", strip=True))
            try: total += float(digits)
            except: pass
    return names, total

async def run(urls, out="async_names.txt", concurrency=100):
    t0 = time.perf_counter()
    sem = asyncio.Semaphore(concurrency)
    conn = aiohttp.TCPConnector(limit=concurrency)
    async with aiohttp.ClientSession(connector=conn, headers=HEADERS) as s:
        tasks = [asyncio.create_task(fetch(s, u, sem)) for u in urls]
        all_names = []
        total_price = 0
        for coro in asyncio.as_completed(tasks):
            try:
                html = await coro
            except Exception:
                continue
            n, p = parse(html)
            all_names.extend(n)
            total_price += p

    with open(out, "w", encoding="utf-8") as f:
        for x in all_names:
            f.write(x + "\n")

    print("Async:", len(urls), "pages,", len(all_names), "products")
    print("Sum:", total_price)
    print("Time:", time.perf_counter() - t0)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("urls_file")
    parser.add_argument("--concurrency", type=int, default=100)
    parser.add_argument("--out", default="async_names.txt")
    a = parser.parse_args()
    urls = [x.strip() for x in open(a.urls_file, encoding="utf-8") if x.strip()]
    asyncio.run(run(urls, out=a.out, concurrency=a.concurrency))
