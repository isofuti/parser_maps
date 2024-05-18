import os
import random
import json
import argparse
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from utils.constants import districts, ACCEPT_BUTTON, type_org_mapping

class LinksCollector:

    def __init__(self,
                 driver,
                 #link='https://yandex.ru/maps/47/nizhny-novgorod/search/Кафе/',
                 #link='https://yandex.ru/maps/47/nizhny-novgorod/search/vkusno_i_tochka/',
                 link='https://yandex.ru/maps/org/tok_bor/34602879882/?ll=88.237472%2C36.568632&mode=search&sctx=ZAAAAAgBEAAaKAoSCQiPNo5Y4FhAEUsgJXZt2U5AEhIJIeS8%2Fw91cUARzt2ul6ZLV0AiBgABAgMEBSgKOABAkE5IAWoCcnWdAc3MTD2gAQCoAQC9AeUalYLCAZQBipf484ABjZqR9IQGudGt6G23%2Fuir%2FQOPt%2FWH8wHt%2FdjS6wO26M%2BAxQaq2resjwa38%2FnJ1gHBrMfUoQGD5q3xjgfcqMXE9QHg4bb98wHYmqeFhgSi1JSmlQTFkciv%2BwOV8N2x6wG%2Fx%2BfI7wOBxrvDuwOOxPurLsmTy9PHBqCFmMj0Bv%2FJt%2Br3Bcfnl%2BbQBc2S7MP1AYICB1RPSyBCT1KKAgCSAgCaAgxkZXNrdG9wLW1hcHOwAgE%3D&sll=88.237472%2C36.568632&sspn=136.870766%2C86.480799&text=TOK%20BOR&z=3.63',
                 #link='https://yandex.ru/maps/10335/tashkent/search/TOK%20BOR/',
                 max_errors=5,
                 accept_button=ACCEPT_BUTTON,
                 accept=False):
        self.driver = driver
        self.slider = None
        self.max_errors = max_errors
        self.link = link
        self.accept_button = accept_button
        self.accept = accept

    def _init_driver(self):
        self.driver.maximize_window()


    def _open_page(self, request):
        self.driver.get(self.link)
        sleep(random.uniform(1, 2))
        #self.driver.find_element(By.CLASS_NAME,'search-form-view__input').click()#send_keys(request)
        #sleep(random.uniform(0.4, 2))
        #self.driver.find_element(By.CLASS_NAME,'input _focused _empty _view_search _size_medium').send_keys(request)
        #sleep(random.uniform(0.4, 0.7))
        #self.driver.find_element(By.CLASS_NAME,'small-search-form-view__button').click()
        # Нажимаем на кнопку поиска
        sleep(random.uniform(1.4, 2))
        self.slider = self.driver.find_element(By.CLASS_NAME,'scroll__scrollbar-thumb')

        if self.accept:
        # Соглашение куки
            flag = True
            count = 0
            while flag:
                try:
                    count += 1
                    sleep(3)
                    self.driver.find_element(By.XPATH, self.accept_button).click()
                    flag = False
                except:
                    if count > 5:
                        self.driver.quit()
                        self._init_driver()
                        self._open_page(request)
                    flag = True


    def run(self, city, district, type_org_ru, type_org):
        self._init_driver()
        request = city + ' ' + district + ' ' + type_org_ru
        self._open_page(request)
        organizations_hrefs = []

        count = 0
        link_number = [0]
        errors = 0
        while self.max_errors > errors:
            try:
                ActionChains(self.driver).click_and_hold(self.slider).move_by_offset(0, int(100/errors)).release().perform()
                slider_organizations_hrefs = self.driver.find_elements(By.CLASS_NAME, 'search-snippet-view__link-overlay')
                slider_organizations_hrefs = [href.get_attribute("href") for href in slider_organizations_hrefs]
                organizations_hrefs = list(set(organizations_hrefs + slider_organizations_hrefs))
                count += 1
                if count % 3 == 0:
                    if len(organizations_hrefs) == link_number[-1]:
                        errors = errors + 1
                    print(len(organizations_hrefs))
                    link_number.append(len(organizations_hrefs))

                sleep(random.uniform(0.05, 0.1))
            except Exception:
                errors = errors + 1
                print('errors', errors)
                sleep(random.uniform(0.3, 0.4))

        directory = f'links/{type_org}'
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.driver.quit()
        with open(f'{directory}/{request}.json', 'w') as file:
            json.dump({'1': organizations_hrefs}, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("type_org", help="organization type")
    args = parser.parse_args()
    type_org = args.type_org

    for type_org in ['charge']:
        for district in ['Алания']:
            sleep(1)
            driver = webdriver.Chrome()
            grabber = LinksCollector(driver)
            grabber.run(city="Узбекистан", district=district, type_org_ru=type_org_mapping[type_org], type_org=type_org)

