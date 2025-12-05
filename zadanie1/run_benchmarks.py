import subprocess
import csv
import time
import json
import os
import sys

SERVERS = {
    "thread": "http://127.0.0.1:8001/parse?url=",
    "async":  "http://127.0.0.1:8002/parse?url="
}

PAGES = [
    "https://dental-first.ru/catalog",
    "https://dental-first.ru/catalog/page/2", 
    "https://dental-first.ru/catalog/page/3"
]


CONCURRENCY = [5, 10, 20]  

RESULT_CSV = "results.csv"

def run_load_test(url, conc, req):
    print(f"  Запуск: concurrency={conc}, requests={req}")
    
    cmd = [sys.executable, "load_client.py", "--url", url, 
           "--concurrency", str(conc), "--requests", str(req),
           "--timeout", "60"] 
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        
        if result.returncode != 0:
            print(f"  Код ошибки: {result.returncode}")
        
        output = result.stdout.strip()
        for line in reversed(output.split('\n')):
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                try:
                    data = json.loads(line)
                    return data
                except:
                    continue
        
        return {"success": 0, "failed": req, "avg_ms": 0, "error": "no valid json"}
        
    except subprocess.TimeoutExpired:
        return {"success": 0, "failed": req, "avg_ms": 0, "error": "timeout"}

def main():
    print("\nНАГРУЗОЧНОЕ ТЕСТИРОВАНИЕ (уменьшенная нагрузка)")

    

    for filename in ["thread_results.txt", "async_results.txt", RESULT_CSV]:
        if os.path.exists(filename):
            os.remove(filename)
    
    rows = []
    
    for server_name, base_url in SERVERS.items():
        print(f"\nТЕСТИРУЕМ: {server_name.upper()}")

        
        for page_url in PAGES:
            print(f"\nСтраница: {page_url}")
            
            for concurrency in CONCURRENCY:
                full_url = base_url + page_url
                print(f"\nколичество одновременных запросов: {concurrency}")
                
                start_time = time.time()
                result = run_load_test(full_url, concurrency, concurrency)
                elapsed = time.time() - start_time
                
                row = {
                    "server": server_name,
                    "page": page_url,
                    "concurrency": concurrency,
                    "elapsed_s": round(elapsed, 3),
                    "success": result.get("success", 0),
                    "failed": result.get("failed", 0),
                    "avg_ms": result.get("avg_ms", 0),
                    "success_rate": round((result.get("success", 0) / concurrency) * 100, 1) 
                            if concurrency > 0 else 0,
                    "error": result.get("error", "")
                }
                
                rows.append(row)
                

                with open(RESULT_CSV, "w", newline='', encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=row.keys())
                    writer.writeheader()
                    writer.writerows(rows)
                
                time.sleep(5)  
    

    print("\nИТОГОВЫЕ РЕЗУЛЬТАТЫ:")

    
    print(f"\n{'Сервер':<10} {'Страница':<30} {'C':<4} {'Время':<6} {'Успешно':<8} "
          f"{'Ошибок':<8} {'Ср.мс':<8} {'%':<6}")
    print("-" * 90)
    
    for row in rows:
        print(f"{row['server']:<10} {row['page'][-30:]:<30} {row['concurrency']:<4} "
              f"{row['elapsed_s']:<6.1f} {row['success']:<8} {row['failed']:<8} "
              f"{row['avg_ms']:<8.1f} {row['success_rate']:<6.1f}")
    

    print("\nФАЙЛЫ С ТОВАРАМИ:")

    
    for filename in ["thread_results.txt", "async_results.txt"]:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
            print(f"{filename}: {len(lines)} записей")
            if lines:
                print(f"  Пример: {lines[0].strip()}")
        else:
            print(f"{filename}: файл не создан")

if __name__ == "__main__":
    main()