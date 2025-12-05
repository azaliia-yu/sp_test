import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import argparse
import re

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; scraper/1.0)"}

def fetch(url, timeout=10):
    r = requests.get(url, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return r.text

def parse_product_names_and_prices(html):
    soup = BeautifulSoup(html, "lxml")
    names = []
    total_price = 0.0
    for card in soup.select(".product-item, .catalog-item, .product-card"):
        title_el = card.select_one(".product-title, .product-name, .item-title")
        price_el = card.select_one(".price, .product-price, .item-price")
        if title_el:
            names.append(title_el.get_text(strip=True))
        if price_el:
            text = price_el.get_text(" ", strip=True)
            digits = re.sub(r"[^\d,\.]", "", text).replace(",", ".")
            try:
                total_price += float(digits)
            except:
                pass
    return names, total_price

def worker(url):
    html = fetch(url)
    return parse_product_names_and_prices(html)

def run(urls, out_file="thread_names.txt", max_workers=10):
    t0 = time.perf_counter()
    all_names = []
    total_price = 0.0
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = [ex.submit(worker, u) for u in urls]
        for f in as_completed(futures):
            try:
                names, price = f.result()
            except Exception as e:
                print("Ошибка:", e)
                continue
            all_names.extend(names)
            total_price += price

    with open(out_file, "w", encoding="utf-8") as fh:
        for n in all_names:
            fh.write(n + "\n")

    t1 = time.perf_counter()
    print(f"Многопоточный: {len(urls)} страниц, товаров {len(all_names)}, сумма {total_price:.2f}")
    print("Время:", t1 - t0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("urls_file")
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--out", default="thread_names.txt")
    args = parser.parse_args()
    with open(args.urls_file, "r", encoding="utf-8") as fh:
        urls = [x.strip() for x in fh if x.strip()]
    run(urls, out_file=args.out, max_workers=args.workers)
