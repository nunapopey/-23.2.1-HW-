import pip
import requests
from bs4 import BeautifulSoup
import pandas as pd

def collect_user_rates(user_login, book_name=None):
    page_num = 1
    data = []
    while True:
        url = f'https://books.yandex.ru/@b1197186777/books/all/{user_login}/votes/'
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'lxml')
        entries = soup.find_all('div', class_='item')

        if len(entries) == 0:  # Признак остановки
            break
        for entry in entries:
            div_book_name = entry.find('div', class_='nameRus')
            div_book_name.find('a').text
            my_rating_div = entry.find('div', class_="vote")
            if my_rating_div is not None:
                my_rating = my_rating_div.text
            else:
                # Элемент не найден
                my_rating = "Элемент не найден"

            data.append({
                'book_name': book_name,
                'my_rating': my_rating
            })

        page_num += 1  # Переходим на следующую страницу
    return data

user_rates = collect_user_rates(input("Введите данные: "))
print(len(user_rates))

df = pd.DataFrame(user_rates)
df.to_excel('user_rates1.xlsx')

def get_rated_films(user_rates):
    rated_book = []
    while True:
        for item in user_rates:
            my_rating = float(item['my_rating'])  # Преобразуем строку в число с плавающей точкой
            if my_rating >= 8:
                rated_book.append(item)
        return rated_book


def get_rated_book(user_rates):
    pass


user_rates_ = get_rated_book(user_rates)
# noinspection PyTypeChecker
print(len(user_rates_))

df = pd.DataFrame(user_rates_)
df.to_excel('user_rates2.xlsx')
