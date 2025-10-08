import os
import requests
import time
import random
from fake_headers import Headers


class HtmlSaver:

    def __init__(self, pagination_limit=300, slow_mode=False):
        self.pagination_limit = pagination_limit
        self.slow_mode = slow_mode


    def get_html_src(self):
        print(f"Начинаю сбор html файлов в количестве {self.pagination_limit}")


        os.makedirs("index", exist_ok=True)
        
        for page in range(1, self.pagination_limit + 1):
            
            url = f"https://new.fips.ru/publication-web/publications/IZPM?pageNumber={page}"\
                "&tab=IZPM&inputSelectOIS=Invention%2CUtilityModel&selectOISDocType=All"\
                "&extendedFilter=true&searchSortSelect=dtPublish&searchSortDirection=true&"\
                "searchTextBox_classifierMpk=B65D%20%2085/804"
            
            headers = Headers(headers=True).generate()

            req = requests.get(url=url, headers=headers)

            with open(f"index/index_{page}.html", 'w') as file:
                file.write(req.text)
            

            print(f"Сохранен html {page} файл страницы из {self.pagination_limit}")


            if self.slow_mode:
                sleep_time = random.randint(1, 5)


                print(f"Куллдаун {sleep_time} сек...")


                time.sleep(sleep_time)
        
        
        print("Сбор html страниц в завершен успешно")



