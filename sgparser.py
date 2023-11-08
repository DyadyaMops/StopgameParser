import requests
import csv
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import threading


def parse(choise):
    
    if choise == '1':
    
        with tqdm(total=859, desc='Прогресс') as pbar:
                csvfile = open('games.csv', 'a', newline='', encoding='utf-8')
                fieldnames = ['Название', 'Рейтинг']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                

                def parse_page(start, stop):
                    nonlocal pbar
                    for page in range(start, stop+1):
                        url = "https://stopgame.ru/games/catalog?p=" + str(page)

                        request = requests.get(url)
                        html = bs(request.content, "lxml")
                        game_card = html.find_all("a", class_ = "_card_2lb1u_1")
                        
                        for game in game_card:
                                game_url = game['href']
                                print("https://stopgame.ru"+game_url)
                                requestToGamePage = requests.get("https://stopgame.ru"+game_url)
                                pageOfGame = bs(requestToGamePage.content, "lxml")

                                game_title = pageOfGame.find("h2")
                            
                                if pageOfGame.find("span", class_ = "_users-rating__total_1jxto_1"):
                                    game_rating = pageOfGame.find("span", class_ = "_users-rating__total_1jxto_1")
                            
                                else:
                                    game_rating = 0
                            
                                if type(game_rating) != int:
                                    game_rating = game_rating.text

                                game_info = {'Название' : game_title.text, 'Рейтинг' : game_rating}
                                writer.writerow(game_info)
                                pbar.update(1)
                    csvfile.close()
                    

                    

                '''threads = []
                for i in range(10):
                    thread = threading.Thread(target=parse_page, args=(i *86, i *86 + 86))
                    thread.start()
                    threads.append(thread)

                for thread in threads:
                    thread.join()
'''             
    parse_page(1,2)
'''
            url = "https://stopgame.ru"

            if choise == '1':

                url += "/games/catalog?p="

                page = 1
            
                while page < 859:


                    url += str(page)

                    request = requests.get(url)
                    html = bs(request.content, "lxml")
                
                    game_card = html.find_all("a", class_ = "_card_2lb1u_1")
                

                    for game in game_card:
                        game_url = game['href']
                        requestToGamePage = requests.get("https://stopgame.ru"+game_url)
                        pageOfGame = bs(requestToGamePage.content, "lxml")

                        game_title = pageOfGame.find("h2")
                    
                        if pageOfGame.find("span", class_ = "_users-rating__total_1jxto_1"):
                            game_rating = pageOfGame.find("span", class_ = "_users-rating__total_1jxto_1")
                    
                        else:
                            game_rating = 0
                    
                        if type(game_rating) != int:
                            game_rating = game_rating.text

                        game_info = {'Название' : game_title.text, 'Рейтинг' : game_rating}
                        writer.writerow(game_info)     

                        
                    
                    page+=1
                    pbar.update(1)

'''



            
                
                    

        
            
        

        
        
        


        

        