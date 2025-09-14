import requests
from bs4 import BeautifulSoup
import pandas as pd

def collect_movie_ratings():
    url = 'https://www.kinoafisha.info/rating/movies/2025/'
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html.parser')

    data = []
    
    entries = soup.find_all('div', class_='movieList_item movieItem movieItem-rating movieItem-position')

    for entry in entries:
        div_film_name = entry.find('div', class_='movieItem_info')
        film_name = div_film_name.find('a').text.strip() if div_film_name and div_film_name.find('a') else 'Не найдено'

        div_rating = entry.find('span', class_='movieItem_itemRating miniRating miniRating-good')
        rating = div_rating.text.strip() if div_rating else 'Не найдено'

        div_genres = entry.find('div', class_='movieItem_details')
        genres = div_genres.find('span').text.strip() if div_genres and div_genres.find('span') else 'Не найдено'

        # Добавляем новую пару ключ-значение
        data.append({'название фильма': film_name, 'жанр': genres, 'рейтинг фильма': rating})

    return data

movie_rates = collect_movie_ratings()

# Создание записи в Excel
df = pd.DataFrame(movie_rates)
df.to_excel('movie_rates_2025.xlsx', index=False)  # Сохраняем файл без индексов

print("Данные успешно сохранены в movie_rates_2025.xlsx")