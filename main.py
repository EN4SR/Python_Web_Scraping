import requests
import selectorlib
import time
import mysql.connector
import datetime
from send_email import send_email

WEBSITE_URL = 'https://programmer100.pythonanywhere.com/tours/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# Connect to database
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="python_db"
)


def scrap(url):
    """Scrape the page source from supplied url"""
    response = requests.get(url, headers=HEADERS)
    source_code = response.text
    return source_code


def extract_data(source):
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value = extractor.extract(source)['tours']
    return value


def save_data(data):
    # Save data to text file
    with open('data.txt', 'a') as file:
        file.write(data + '\n')

    # Save data to Database (MySQL)
    cursor = mydb.cursor()
    data_list = data.split(',')
    band, city, date = [item.strip() for item in data_list]
    d, m, y = date.split('.')
    date = f"{y}-{m}-{d}"
    print(date)
    sql = "INSERT INTO events (band_name, city, date) VALUES (%s, %s, %s)"
    val = (band,
           city,
           date)
    cursor.execute(sql, val)
    mydb.commit()
    print(cursor.rowcount, "record inserted.")


def read_data():
    # with open('data.txt', 'r') as file:
    #     return file.read()

    # Read data from database
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM events")
    result = cursor.fetchall()
    return result


def send_email(message):
    print('Email was sent with: ' + message)
    # send_email(message)


if __name__ == '__main__':
    while True:
        page_source = scrap(WEBSITE_URL)
        data = extract_data(page_source)
        print(data)

        if data != 'No upcoming tours':
            saved_data = read_data()
            # print(saved_data)
            if data not in saved_data:
                save_data(data)
                # send_email(data)

        time.sleep(2)