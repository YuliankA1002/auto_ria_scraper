#  AutoRia Scraper 🚗

Цей проєкт — це Scrapy-додаток для щоденного скрапінгу вживаних авто з [auto.ria.com](https://auto.ria.com/car/used/), збереження результатів у базу даних PostgreSQL та створення SQL-дампу.

---

##  Встановлення
1. **Клонувати репозиторій:**

```bash
   git clone https://github.com/yourname/autoria_scraper.git
   cd autoria_scraper
```

2. **Створити та активувати віртуальне середовище:**

```bash
python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate     # для Windows
```

3. **Встановити залежності:**

```bash
pip install -r requirements.txt
```
4. **Створити .env файл** з параметрами доступу до PostgreSQL і налаштуваннями для scheduler на основі файлу .env_example

5. **Переконатися, що встановлений pg_dump:**

```bash
pg_dump --version
```
##  **Запуск парсера**

**Запустити спайдер вручну** (рекомендується через run_spider.py, який підвантажує .env):

```bash
python scripts/run_spider.py
```

##  **Дамп бази даних**
Вручну можна запустити наступною командою:

```bash
python scripts/dump_db.py
```
**Локація дампу:**

SQL-файли зберігаються в папці dumps/ у вигляді:

```bash
dumps/dump_YYYYMMDD_HHMMSS.sql
```

## Запуск за розкладом

Автоматичний запуск скрапера і створення дампу бази щодня о SCRAPE_TIME та DUMP_TIME відповідно, можна зробити наступною командою:
```bash
python run_scheduler.py
```
