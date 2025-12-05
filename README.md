# sp_test

## Структура проекта

zadanie1/      # HTTP-серверы и парсер
zadanie2/      # Сокеты и клиент
README.md

---

## Задание 1 — HTTP-серверы

1. Установить зависимости:
```
cd zadanie1
pip install -r requirements.txt
```

3. Очисите результаты
```
python clear_results.py
```

4. Запустите серверы в разных терминалах
 Терминал 1:
```
python thread_server.py
```

 Терминал 2:
 ```
python async_server.py
```

4. Запустите бенчмарки (в Терминале 3):
```
python run_benchmarks.py
```

6. Проверьте результаты
```
cat thread_results.txt | head -20  # первые 20 названий из многопоточного сервера
cat async_results.txt | head -20    # первые 20 названий из асинхронного сервера
cat results.csv                     # сравнение производительности
```
---

## Задание 2 — Сокеты

1. Запустить серверы в разных терминалах:
```
python thread_socket_server.py   # порт 9001
python async_socket_server.py    # порт 9002
```

3. Проверка клиента:
```
python socket_client.py .
```

5. Запуск нагрузочного теста:
```
python run_socket_benchmarks.py
Результаты → socket_results.csv
```
---



