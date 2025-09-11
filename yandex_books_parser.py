import pip
import requests
from bs4 import BeautifulSoup
import pandas as pd

def collect_user_rates(user_login):
    page_num = 1
    data = []
    while True:
        url = f'https://books.yandex.ru/@{user_login}/votes/'  # Убедитесь, что user_login соответствует формату
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'lxml')
        entries = soup.find_all('div', class_='item')

        if len(entries) == 0:  # Признак остановки
            break

        for entry in entries:
            div_book_name = entry.find('div', class_='nameRus')
            if div_book_name:
                book_name = div_book_name.find('a').text  # Извлекаем название книги
            else:
                book_name = "Название не найдено"  # Элемент не найден

            my_rating_div = entry.find('div', class_="vote")
            if my_rating_div is not None:
                my_rating = my_rating_div.text.strip()  # Убираем лишние пробелы
            else:
                my_rating = "Элемент не найден"  # Элемент не найден

            data.append({
                'book_name': book_name,
                'my_rating': my_rating
            })

        page_num += 1  # Переходим на следующую страницу
    
    return data

user_login = input("Введите логин пользователя: ")
user_rates = collect_user_rates(user_login)

print(len(user_rates))

df = pd.DataFrame(user_rates)
df.to_excel('user_rates1.xlsx', index=False)  # Сохраняем файл без индексов

def get_rated_books(user_rates):
    rated_books = []
    for item in user_rates:
        try:
            my_rating = float(item['my_rating'])  # Преобразуем строку в число с плавающей точкой
            if my_rating >= 8:
                rated_books.append(item)
        except ValueError:
            continue  # Пропускаем, если значение не может быть преобразовано

    return rated_books

user_rates_above_8 = get_rated_books(user_rates)

print(len(user_rates_above_8))

df_filtered = pd.DataFrame(user_rates_above_8)
df_filtered.to_excel('user_rates2.xlsx', index=False)  # Сохраняем файл без индексов
