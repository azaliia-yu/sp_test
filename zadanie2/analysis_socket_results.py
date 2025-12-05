import csv
import matplotlib.pyplot as plt


thread_results = []
async_results = []

with open('socket_results.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['server_port'] == '9001':
            thread_results.append((int(row['concurrency']), float(row['elapsed_s'])))
        else:
            async_results.append((int(row['concurrency']), float(row['elapsed_s'])))


print("АНАЛИЗ РЕЗУЛЬТАТОВ СРАВНЕНИЯ СОКЕТ-СЕРВЕРОВ")


for (conc1, time1), (conc2, time2) in zip(thread_results, async_results):
    diff_percent = ((time2 - time1) / time1) * 100
    print(f"Количество запросов: {conc1}:")
    print(f"  Многопоточный: {time1:.3f} сек")
    print(f"  Асинхронный:  {time2:.3f} сек")
    print(f"  Разница: {diff_percent:+.1f}%\n")


last_thread = thread_results[-1]  
last_async = async_results[-1]    

estimated_thread_1000 = last_thread[1] * 2  
estimated_async_1000 = last_async[1] * 2    

print("\nЭКСТРАПОЛЯЦИЯ НА 1000 ЗАПРОСОВ:")
print(f"Многопоточный сервер: ~{estimated_thread_1000:.1f} сек")
print(f"Асинхронный сервер:  ~{estimated_async_1000:.1f} сек")
print("\nОЦЕНКА ПАМЯТИ:")
print("- Многопоточный: 8-13 ГБ (1000 потоков × 8-13 МБ каждый)")
print("- Асинхронный:   8-10 МБ (1000 корутин × 2-3 КБ + буферы)")