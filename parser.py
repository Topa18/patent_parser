import os
import shutil
import csv
import pandas as pd
from bs4 import BeautifulSoup
from html_saver import HtmlSaver


class Parser:

    def __init__(self, html_saver: HtmlSaver, upd_indexes=False):
        self.html_saver = html_saver
        self.upd_indexes = upd_indexes

    
    def prep_csv_file(self):
        with open('result.csv', 'w', encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(('Номер патента', 'Имя патента', 'Номер заявки',
                             'Дата подачи заявки', 'Дата публикации', 'Дата регистрации',
                             'Ccылка на патент'))


    def collect_data(self):
        if self.upd_indexes:
            shutil.rmtree('index')
            self.html_saver.get_html_src()

        pages = len(os.listdir('index'))

        for file in os.listdir('index'):
            print(f"Собираю данные с {file}...\n")


            with open(f"index/{file}") as cur_index:
                src = cur_index.read()

            soup = BeautifulSoup(src, "lxml")

            table = soup.find("table", class_="table").find_all('tr')
            
            patent_data = []
            all_data = []

            # counter = 0 Для fline
            # counter = 1 для middle
            # counter = 2 для lastline
            counter = 3
            for data in table:
                if counter == 3:
                    counter = 0 
                    patent_data = []
                    continue

                if counter == 0:
                    fline_data = data.find_all('a')
                    for d in fline_data:
                        cleaned_data = ' '.join(d.text.strip().split())
                        patent_data.append(cleaned_data)
                    counter += 1
                    continue

                if counter == 1:
                    middle_data = data.find_all("span", class_="mobileblock")
                    for d in middle_data:
                        cleaned_data = ' '.join(d.text.strip().split())
                        cleaned_data = cleaned_data.replace('Номер заявки: ', '')
                        cleaned_data = cleaned_data.replace('Дата подачи заявки: ', '')
                        patent_data.append(cleaned_data)
                    counter += 1
                    continue

                if counter == 2:
                    lastline_data = data.find_all("span", class_="gray mobileblock")
                    for d in lastline_data:
                        cleaned_data = ' '.join(d.text.strip().split())
                        cleaned_data = cleaned_data.replace('Публикация: ', '')
                        cleaned_data = cleaned_data.replace('Регистрация: ', '')
                        patent_data.append(cleaned_data)
                    patent_href = data.find('a').get('href')
                    patent_data.append(patent_href)
                    counter += 1
                
                all_data.append(patent_data)


            with open('result.csv', 'a', encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                for d in all_data:
                    writer.writerow(d)
            
            print(f"Данные записаны в result.csv\nПерехожу к следующему индексу\n\n")

        print("Парсинг завершен!")


    def convert_csv_to_xlsx(self, path_to_csv: str, output_xlsx_path: str):

        df = pd.read_csv(path_to_csv)
        df.to_excel(output_xlsx_path, index=False)

        print('Файл сконверитирован успешно\nВыполнение окончено!')