# sp_test

## Структура проекта

zadanie1/      # HTTP-серверы и парсер
zadanie2/      # Сокеты и клиент
README.md

---

## Задание 1 — HTTP-серверы

1. Установить зависимости:
cd zadanie1
pip install -r requirements.txt

2. Запустить сервера в разных терминалах:
python thread_server.py    # многопоточный
python async_server.py     # асинхронный

3. Проверить вручную:
curl "http://127.0.0.1:8001/parse?url=https://dental-first.ru/catalog"
curl "http://127.0.0.1:8002/parse?url=https://dental-first.ru/catalog"

4. Запустить нагрузочный тест:
python run_benchmarks.py
Результаты → results.csv  
Названия товаров → thread_results.txt, async_results.txt

---

## Задание 2 — Сокеты

1. Запустить серверы в разных терминалах:
python thread_socket_server.py   # порт 9001
python async_socket_server.py    # порт 9002

2. Проверка клиента:
python socket_client.py .

3. Запуск нагрузочного теста:
python run_socket_benchmarks.py
Результаты → socket_results.csv

---



