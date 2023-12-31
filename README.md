# StopgameParser

## StopgameParser - это многопоточный, асинхронный парсер сайта [Stopgame](https://www.stopgame.ru)

![](https://images.stopgame.ru/news/2018/12/11/NBt0J1U.jpg)

Данный парсер сохраняет полученные данные в формате CSV, что позволяет в дальнейшем удобно их обрабатывать

Парсинг доступен для следующих страниц:

1) [Игры](https://stopgame.ru/games/catalog?p=1)
2) [Блоги](https://stopgame.ru/games/catalog?p=1)
3) [Новости](https://stopgame.ru/games/catalog?p=1)

- Игры сохраняются в формате **Название,Рейтинг**
- Блоги в формате **Рейтинг,Заголовок,Ссылка**
- Новости в формате **Заголовок,Ссылка**

Каждому итоговому файлу присваивается имя в виде *unix время_страница*

Например 1699604877_n.csv - где цифры - время, n - раздел новости

## Время работы

Время работы парсера зависит в первую очередь от вашего интернет-соединения. При хорошей скорости (100Мб/c) парсинг
игр занимает около 25-30 минут (869 страниц + запросы на каждую страницу конкретной игры).

Время парсинга блогов и новостей примерно одинаковое и составляет 10-15 минут (более 2000 страниц)

## Установка 

Для установки последовательно выполните следующие команды:
```Bash
git clone https://github.com/DyadyaMops/StopgameParser.git
cd StopgameParser.git
pip install -r reqs.txt
python main.py
```

При запуске появится меню. Просто введите цифру, соответствующую нужной опции

![image](https://github.com/DyadyaMops/StopgameParser/assets/115101419/0e1253f2-c116-4853-98e1-e2d47925004b)

