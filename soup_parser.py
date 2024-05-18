from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, MoveTargetOutOfBoundsException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import re


class SoupContentParser(object):

    def get_name(self, soup_content):
        name = ""
        try:
            # Попытка найти имя с первым классом
            name_element = soup_content.find("h1", {"class": "orgpage-header-view__header"})
            if not name_element:  # Если элемент не найден, попробуйте другой класс
                name_element = soup_content.find("h1", {"class": "_tvxwjf"})  
            if name_element:
                name = name_element.getText().strip()
        except Exception as e:
            print(f"Ошибка при извлечении имени: {e}")
            return ""

        return name

    def get_phone(self, soup_content):
        phones = []
        try:
            for data in soup_content.find_all("div", {"class": "card-phones-view__number"}):
                phone = data.getText().strip()
                if phone:  # Проверка наличия номера телефона
                    phones.append(phone)
            for data in soup_content.find_all("div", {"class": "_b0ke8"}):
                link = data.find('a')
                if link:
                    phone = link.get('href')
                    if phone:  # Проверка наличия ссылки
                        phones.append(phone)
        except Exception as e:
            print(f"Ошибка при извлечении телефонных номеров: {e}")
            return []  # Возвращаем пустой список в случае ошибки
        return phones

    def get_social(self, soup_content):
        socials = []
        try:
            for data in soup_content.find_all("a", {"class": "button _view_secondary-gray _ui _size_medium _link"}):
                href = data.get('href')
                if href:  # Проверка наличия ссылки
                    socials.append(href)
            for data in soup_content.find_all("div", {"class": "_14uxmys"}):
                link = data.find('a')
                if link and link.get('href'):  # Проверка наличия элемента и ссылки
                    socials.append(link.get('href'))
        except Exception as e:
            print(f"Ошибка при извлечении социальных ссылок: {e}")
            return []  # Возвращаем пустой список в случае ошибки

        return socials

    def get_address(self, soup_content):
        addresses = []  # Инициализация списка для хранения всех адресов
        try:
            # Поиск и добавление адресов из тегов <a> с классом "business-contacts-view__address-link"
            for data in soup_content.find_all("a", {"class": "business-contacts-view__address-link"}):
                if data.getText().strip():  # Добавляем только непустые строки
                    addresses.append(data.getText().strip())
            # Поиск и добавление адресов из тегов <span> с классом "_er2xx9"
            for data in soup_content.find_all("span", {"class": "_er2xx9"}):
                links = data.find_all('a', {"class": "_2lcm958"})
                for link in links:
                    if link.getText().strip():  # Добавляем только непустые строки
                        addresses.append(link.getText().strip())
        except Exception as e:
            print(f"Произошла ошибка при обработке адресов: {e}")
            return ""  # Возвращаем пустую строку в случае ошибки
        # Преобразование списка адресов в одну строку, разделенную запятыми
        address_string = ', '.join(addresses)
        return address_string

    def get_website(self, soup_content):
        try:
            for data in soup_content.find_all("span", {"class": "business-urls-view__text"}):
                website = data.getText()
            return website
        except Exception:
            return ""

    def get_opening_hours(self, soup_content):
        opening_hours = []
        try:
            for data in soup_content.find_all("meta", {"itemprop": "openingHours"}):
                opening_hours.append(data.get('content'))
            return opening_hours
        except Exception:
            return ""

    def get_goods(self, soup_content):
        dishes = []
        prices = []
        try:
            for dish_s in soup_content.find_all("div", {"class": "related-item-photo-view__title"}):
                dishes.append(dish_s.getText())

            for price_s in soup_content.find_all("span", {"class": "related-product-view__price"}):
                prices.append(price_s.getText())

            for dish_l in soup_content.find_all("div", {"class": "related-item-list-view__title"}):
                dishes.append(dish_l.getText())

            for price_l in soup_content.find_all("div", {"class": "related-item-list-view__price"}):
                prices.append(price_l.getText())

        except NoSuchElementException:
            try:
                for dish_l in soup_content.find_all("div", {"class": "related-item-list-view__title"}):
                    dishes.append(dish_l.getText())

                for price_l in soup_content.find_all("div", {"class": "related-item-list-view__price"}):
                    prices.append(price_l.getText())
            except Exception:
                pass
        except Exception:
            return ""

        return dict(zip(dishes, prices))

    def get_rating(self, soup_content):
        rating = ""
        try:
            for data in soup_content.find_all("span", {"class": "business-summary-rating-badge-view__rating-text"}):
                rating += data.getText()
            for data in soup_content.find_all("div", {"class": "_y10azs"}):
                rating += data.getText()
            return rating
        except Exception:
            return ""

    def get_reviews(self, soup_content, driver):
        reviews = []
        slider = driver.find_element(By.CLASS_NAME,'scroll__scrollbar-thumb')
        try:
            reviews_count = int(soup_content.find_all("div", {"class": "tabs-select-view__counter"})[-1].text)
        except ValueError:
            reviews_count = 0
        except AttributeError:
            reviews_count = 0
        except Exception:
            return ""

        if reviews_count > 150:
            find_range = range(100)
        else:
            find_range = range(30)

        for i in find_range:
            try:
                ActionChains(driver).click_and_hold(slider).move_by_offset(0, 50).release().perform()

            except MoveTargetOutOfBoundsException:
                break

        try:
            soup_content = BeautifulSoup(driver.page_source, "lxml")
            for data in soup_content.find_all("div", {"class": "business-review-view__body-text _collapsed"}):
                reviews.append(data.getText())

            return reviews
        except Exception:
            return ""
