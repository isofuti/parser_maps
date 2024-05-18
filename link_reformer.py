import json
import re

def extract_links(text):
    # Используем регулярное выражение для поиска всех ссылок, начинающихся с http:// или https://
    pattern = r'https?://[a-zA-Z0-9./_-]+'
    return re.findall(pattern, text)

def save_links_to_json(input_text, output_file):
    # Извлекаем ссылки из текста
    links = extract_links(input_text)
    
    # Фильтруем ссылки, содержащие 'yandex.ru/maps'
    filtered_links = [link for link in links if 'yandex.ru/maps' in link or '2gis.ru' in link]
    
    # Создаем словарь для последующей записи в JSON
    links_dict = {"1": filtered_links}
    
    # Записываем в JSON файл
    with open(output_file, 'w') as file:
        json.dump(links_dict, file, indent=4)

# Пример использования функции
input_text = """
https://2gis.ru/voronezh/firm/70000001053023322
"""
output_file = '2gis-links.json'

save_links_to_json(input_text, output_file)

