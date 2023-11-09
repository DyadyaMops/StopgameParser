import csv
import httpx
from bs4 import BeautifulSoup
import re
import time
import os

from tqdm import tqdm


BASE_URL = 'https://stopgame.ru'

GAMES_CATALOG_URL = 'https://stopgame.ru/games/catalog?p={}'  # url страницы из каталога игр
GAME_DEFAULT_URL = 'https://stopgame.ru{}'  # url отдельной игры

BLOGS_URL = 'https://stopgame.ru/blogs/all/p{}'  # url страницы блогов

NEWS_URL = 'https://stopgame.ru/news/all/p{}'  # url страницы новостей


async def get_pages_count(client, url: str):
    """
    Функция возвращает общее количество страниц в разделе
    :param client: AsyncClient httpx
    :param url: url раздела
    :return: количество страниц: int
    """

    resp = await client.get(url)

    page_data = BeautifulSoup(resp.text, 'html.parser')
    main_block = page_data.find(attrs={'id': 'main-content'})

    nav_block = main_block.find(class_='_buttons-row_180tx_17')

    pages = int(nav_block.find_all('a')[-3].text)

    return pages


async def load_to_csv(data: list, fieldnames: list, data_type: str):
    """
    Функция загружает полученные данные в .csv файл
    :param data: массив словарей
    :param fieldnames: заголовки в файле
    :param data_type: тип данных - games / blogs / news
    :return:
    """
    unixtime = int(time.time())  # время создания файла в unix-формате

    if not os.path.exists(data_type):  # если папки нет, то создать ее
        os.makedirs(data_type)

    # создание нового файла: data_type - папка файла, data_type[0] - флажок по первой букве папки для различия файлов
    file_name = f'{data_type}/{unixtime}_{data_type[0]}.csv'

    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for item in data:
            writer.writerow(item)

    return file_name


async def get_game_info(client, game_url: str):
    """
    Получение информации по конкретной игре
    :param client: AsyncClient httpx
    :param game_url: url игры
    :return: словарь данных по игре формата {'Название': str, 'Рейтинг': float}
    """

    try:
        resp = await client.get(GAME_DEFAULT_URL.format(game_url))

        page_data = BeautifulSoup(resp.text, 'html.parser')
        main_block = page_data.find(attrs={'id': 'main-content'})

        game_name = ''
        try:
            game_name = str(main_block.find(class_='_title_1hh2w_171'))

            # очистка от лишних символов
            clean = re.compile('<.*?>')
            game_name = str(re.sub(clean, '', game_name)).strip()
        except:
            pass

        game_rate = 0
        try:  # если игра еще не вышла, то у нее нет оценки
            game_rate = float(main_block.find(class_='_users-rating__total_1hh2w_1').text)
        except:
            pass

        return {'Название': game_name, 'Рейтинг': game_rate}
    except:
        return {'Название': '', 'Рейтинг': ''}


async def parse_games():
    """
    Парсинг игр
    :return: путь к результирующему файлу игр
    """

    file_name = ''

    async with httpx.AsyncClient(http2=True) as client:

        try:

            pages = await get_pages_count(client, GAMES_CATALOG_URL.format(1))  # нахождение количества страниц

            all_games = []

            with tqdm(total=pages, desc='Прогресс') as pbar:

                for i in range(1, pages+1):

                    resp = await client.get(GAMES_CATALOG_URL.format(i))
                    page_data = BeautifulSoup(resp.text, 'html.parser')

                    main_block = page_data.find(attrs={'id': 'main-content'})

                    games = main_block.find(attrs={'id': 'w0'}).find(class_='_games-grid_6d5zv_320').find_all('div', recursive=False)

                    for game in games:

                        try:
                            game_url = game.find('a')['href']

                            game_data = await get_game_info(client, game_url)  # получение информации по игре

                            all_games.append(game_data)
                        except:
                            all_games.append({'Название': '', 'Рейтинг': ''})

                    pbar.update(1)

            file_name = await load_to_csv(all_games, ['Название', 'Рейтинг'], 'games')

        except:
            pass

        return file_name


async def parse_blogs():
    """
    Парсинг блогов
    :return: путь к результирующему файлу блогов
    """

    file_name = ''

    async with httpx.AsyncClient(http2=True) as client:

        try:

            pages = await get_pages_count(client, BLOGS_URL.format(1))  # нахождение количества страниц

            all_blogs = []

            with tqdm(total=pages, desc='Прогресс') as pbar:

                for i in range(1, pages+1):

                    resp = await client.get(BLOGS_URL.format(i))
                    page_data = BeautifulSoup(resp.text, 'html.parser')

                    main_block = page_data.find(attrs={'id': 'main-content'})

                    blogs = main_block.find(attrs={'id': 'w0'}).find('div').find_all('div', recursive=False)

                    for blog in blogs:

                        blog_rate = 0.0
                        try:
                            blog_rate = blog.find('article').find('div').text
                        except:
                            pass

                        blog_main_data = blog.find(class_='_card__title_6bcao_1')

                        blog_url = ''
                        try:
                            blog_url = BASE_URL + str(blog_main_data['href'])
                        except:
                            pass

                        blog_title = ''
                        try:
                            blog_title = str(blog_main_data.text).strip()
                        except:
                            pass

                        all_blogs.append({'Рейтинг': blog_rate, 'Заголовок': blog_title, 'Ссылка': blog_url})

                    pbar.update(1)

            file_name = await load_to_csv(all_blogs, ['Рейтинг', 'Заголовок', 'Ссылка'], 'blogs')
        except:
            pass

        return file_name


async def parse_news():
    """
    Парсинг новостей
    :return: путь к результирующему файлу блогов
    """

    file_name = ''

    async with httpx.AsyncClient(http2=True) as client:

        try:

            pages = await get_pages_count(client, NEWS_URL.format(1))  # нахождение количества страниц

            all_news = []

            with tqdm(total=pages, desc='Прогресс') as pbar:

                for i in range(1, pages+1):

                    resp = await client.get(NEWS_URL.format(i))
                    page_data = BeautifulSoup(resp.text, 'html.parser')

                    main_block = page_data.find(attrs={'id': 'main-content'})

                    news = main_block.find(attrs={'id': 'w0'}).find('div').find_all('div', recursive=False)

                    for new in news:

                        new_block = new.find(class_='_title_11mk8_60')

                        new_title = ''
                        try:
                            new_title = str(new_block.text).strip()
                        except:
                            pass

                        new_url = ''
                        try:
                            new_url = BASE_URL + str(new_block['href'])
                        except:
                            pass

                        all_news.append({'Заголовок': new_title, 'Ссылка': new_url})

                    pbar.update(1)

            file_name = await load_to_csv(all_news, ['Заголовок', 'Ссылка'], 'news')

        except:
            pass

        return file_name
