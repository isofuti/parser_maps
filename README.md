# parser_maps
![plot](img.png)
## Parsing Yandex Maps 'https://yandex.ru/maps'
### Simple start
1. change ```type_org_mapping``` from [constants.py](https://github.com/artemsteshenko/parser_maps/blob/master/utils/constants.py), (```type_org_mapping = 'folder name': 'query'``` For example, ```type_org_mapping = 'showroom': 'Шоу-рум'```)


```
pip3 install -r requirements.txt
python goodinie.py showroom
```
