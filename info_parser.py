import os
import json
import random
import argparse

from time import sleep

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

from soup_parser import SoupContentParser
from utils import json_pattern


class Parser:

    def __init__(self, driver):
        self.driver = driver
        self.soup_parser = SoupContentParser()

    def parse_data(self, hrefs, type_org):
        self.driver.maximize_window()
        self.driver.get('https://yandex.ru/maps')
        parent_handle = self.driver.window_handles[0]
        org_id = 0
        outputs = []

        for organization_url in hrefs:
            #try:
            # if True:
                self.driver.execute_script(f'window.open("{organization_url}","org_tab");')
                child_handle = [x for x in self.driver.window_handles if x != parent_handle][0]
                self.driver.switch_to.window(child_handle)
                sleep(0.7)
                soup = BeautifulSoup(self.driver.page_source, "lxml")
                org_id += 1
                print(org_id)
                #print(type(org_id))
                name = self.soup_parser.get_name(soup)
                if name == "":
                    name = "Без названия"
                address = self.soup_parser.get_address(soup)
                if address == "":
                    print(address)
                    print(type(address))
                    address = "Без адреса"
                website = self.soup_parser.get_website(soup)
                if website == "":
                    website = "Без сайта"
                opening_hours = self.soup_parser.get_opening_hours(soup)
                if opening_hours == []:
                    opening_hours = "Без часов работы"
                ypage = self.driver.current_url
                rating = self.soup_parser.get_rating(soup)
                if rating == "":
                    frating = "Без рейтинга"
                else:
                    rating = rating.replace(',', '.')
                    frating = float(rating)
                social = self.soup_parser.get_social(soup)
                if social == []:
                    social = "Без соц. сетей"
                phone = self.soup_parser.get_phone(soup)
                if phone == []:
                    phone = "Без номера телефона"
                #reviews = self.soup_parser.get_reviews(soup, driver)
                #if reviews == []:
                #    reviews= "Без отзывов"
                reviews = None
                goods = None

                print("Название: ", name, type(name), '\n', "Адрес: ", address, type(address), "\n", "Сайт: ", website, type(website), "\n", "Часы работы: ", opening_hours, type(opening_hours), "\n", "Рейтинг: ", frating, type(frating), "\n", "Соц. сети: ", social, type(social), "\n", "Номер: ", phone, type(phone))

                output = json_pattern.into_json(org_id, name, address, website, opening_hours, ypage, goods, frating,
                                                reviews, phone, social)
                #output = json_pattern.into_json(org_id, name)
                outputs.append(output)

                if org_id == len(hrefs):
                    df = pd.DataFrame()
                    df['outputs'] = outputs
                    df.to_csv(f'result_output/{type_org}_outputs.csv')
                    self.driver.quit()
                    sleep(random.uniform(2.2, 2.4))
                    self.driver = webdriver.Chrome()
                    self.driver.maximize_window()
                    self.driver.get('https://yandex.ru/maps')
                    parent_handle = self.driver.window_handles[0]
                print(f'Данные добавлены, id - {org_id}')

                self.driver.switch_to.window(parent_handle)
                sleep(random.uniform(0.2, 0.4))

            #except:
                #print('Ошибка')
                #print()
                # driver.quit()
                #sleep(random.uniform(2.2, 2.4))
                #self.driver = webdriver.Chrome()
                #self.driver.maximize_window()
                #self.driver.get('https://yandex.ru/maps')
                #parent_handle = self.driver.window_handles[0]
        print('Данные сохранены')
        self.driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("type_org", help="organization type")
    args = parser.parse_args()
    type_org = args.type_org

    all_hrefs = []
    files = os.listdir(f'links/{type_org}')
    for file in files:
        with open(f'links/{type_org}/{file}', 'r', encoding='utf-8') as f:
            hrefs = json.load(f)['1']
            all_hrefs += hrefs
    all_hrefs = list(set(all_hrefs))
    print('all_hrefs', len(all_hrefs))


    driver = webdriver.Chrome()
    parser = Parser(driver)
    parser.parse_data(all_hrefs, type_org)