import schedule
import time
import os
from dotenv import load_dotenv
from scripts.dump_db import dump_db
from scripts.run_spider import run_spider

load_dotenv()


schedule.every().day.at(os.getenv("SCRAPE_TIME")).do(run_spider)
schedule.every().day.at(os.getenv("DUMP_TIME")).do(dump_db)

print("Scheduler started...")
while True:
    schedule.run_pending()
    time.sleep(60)
