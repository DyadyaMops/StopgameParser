from module import *


async def banner():
    """
    Функция выводит приветствие в консоль
    """
    print(
        """
        ███████╗████████╗ ██████╗ ██████╗  ██████╗  █████╗ ███╗   ███╗███████╗
        ██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝ ██╔══██╗████╗ ████║██╔════╝
        ███████╗   ██║   ██║   ██║██████╔╝██║  ███╗███████║██╔████╔██║█████╗  
        ╚════██║   ██║   ██║   ██║██╔═══╝ ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  
        ███████║   ██║   ╚██████╔╝██║     ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗
        ╚══════╝   ╚═╝    ╚═════╝ ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
    
        ██████╗  █████╗ ██████╗ ███████╗███████╗██████╗                       
        ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗                      
        ██████╔╝███████║██████╔╝███████╗█████╗  ██████╔╝                      
        ██╔═══╝ ██╔══██║██╔══██╗╚════██║██╔══╝  ██╔══██╗                      
        ██║     ██║  ██║██║  ██║███████║███████╗██║  ██║                      
        ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝                      
        """)

    print("Добро пожаловать в парсер сайта stopgame.ru!")


async def menu():
    """
    Функция выводит меню в консоль с вариантом выбора 1 - парсинг игр, 2 - парсинг блогов, 3 - парсинг новостей,
        exit - выйти
    """
    print("""

    Для выбора действия просто введите соответствующую цифру      

    +----------------------------------+     
    | 1. | Спарсить раздел ИГРЫ        |
    |----|-----------------------------|
    | 2. | Спарсить раздел БЛОГИ       |
    |----|-----------------------------|     
    | 3. | Спарсить раздел НОВОСТИ     |
    +----------------------------------+

    для выхода введите exit 

    """)

    choice = input(">>> ")

    if choice == '1':  # выбор парсинга игр

        res = await parse_games()
        print(f'Файл с результатом парсинга игр доступен в {res}')

    elif choice == '2':  # выбор парсинга блогов

        res = await parse_blogs()
        print(f'Файл с результатом парсинга блогов доступен в {res}')

    elif choice == '3':  # выбор парсинга новостей

        res = await parse_news()
        print(f'Файл с результатом парсинга новостей доступен в {res}')

    else:

        exit()
