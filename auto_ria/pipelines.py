import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


class PostgresPipeline:

    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        self.cur = self.conn.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                url TEXT PRIMARY KEY,
                title TEXT,
                price_usd INTEGER,
                odometer INTEGER,
                username TEXT,
                phone_number TEXT,
                image_url TEXT,
                images_count INTEGER,
                car_number TEXT,
                car_vin TEXT,
                datetime_found TIMESTAMP
            )
        ''')
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        self.cur.execute("SELECT 1 FROM cars WHERE url=%s", (item['url'],))
        if self.cur.fetchone():
            return item

        self.cur.execute('''
            INSERT INTO cars (
                url, title, price_usd, odometer, username,
                phone_number, image_url, images_count,
                car_number, car_vin, datetime_found
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''', (
            item['url'],
            item['title'],
            item['price_usd'],
            item['odometer'],
            item['username'],
            item['phone_number'],
            item['image_url'],
            item['images_count'],
            item['car_number'],
            item['car_vin'],
            item['datetime_found']
        ))
        return item
