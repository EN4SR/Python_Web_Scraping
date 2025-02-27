import requests
import selectorlib
import time
from send_email import send_email

WEBSITE_URL = 'https://programmer100.pythonanywhere.com/tours/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


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
    with open('data.txt', 'a') as file:
        file.write(data + '\n')


def read_data():
    with open('data.txt', 'r') as file:
        return file.read()


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
            if data not in saved_data:
                save_data(data)
                send_email(data)

        time.sleep(5)