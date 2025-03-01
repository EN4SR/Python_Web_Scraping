import requests
import selectorlib
import time
import mysql.connector
import datetime
from send_email import send_email

WEBSITE_URL = 'https://programmer100.pythonanywhere.com/tours/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

class Event:
    def scrap(self, url):
        """Scrape the page source from supplied url"""
        response = requests.get(url, headers=HEADERS)
        source_code = response.text
        return source_code

    def extract_data(self, source):
        extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
        value = extractor.extract(source)['tours']
        return value

class Database:
    def __init__(self, host="localhost", user="root", password="", db=""):
        self.mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db
        )

    def save(self, data):
        # Save data to Database (MySQL)
        cursor = self.mydb.cursor()
        data_list = data.split(',')
        band, city, date = [item.strip() for item in data_list]
        d, m, y = date.split('.')
        date = f"{y}-{m}-{d}"
        sql = "INSERT INTO events (band_name, city, date) VALUES (%s, %s, %s)"
        val = (band,
               city,
               date)
        cursor.execute(sql, val)
        self.mydb.commit()
        # print(cursor.rowcount, "record inserted.")

    def read(self):
        # Read data from database
        cursor = self.mydb.cursor()
        cursor.execute("SELECT * FROM events")
        result = cursor.fetchall()
        return result


if __name__ == '__main__':
    while True:
        event = Event()
        page_source = event.scrap(WEBSITE_URL)
        data = event.extract_data(page_source)
        print(data)

        if data != 'No upcoming tours':
            database = Database(db="python_db")
            saved_data = database.read()
            items = []

            for item in saved_data:
                _i, name, city, date = item

                y, m, d = str(date).split('-')
                date = f"{d.strip('0')}.{m.strip('0')}.{y}"
                items.append(f"{name.strip()}, {city.strip()}, {date}")

            if data not in items:
                database.save(data)
                print("1 event record inserted")
            else:
                print('Event already saved')

        time.sleep(2)