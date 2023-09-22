# -*- coding: utf-8 -*-
import requests
from tqdm import tqdm
import cookies_and_header
import pandas as pd


def get_data():
    cards = {}
    #count_of_pages = int(input('Введите, сколько парсить страниц и нажмите ENTER: '))
    count_of_pages = 1
    cities = {'RU-AD':'Адыгея', 'RU-AL':'Республика Алтай', 'RU-ALT':'Алтайский край', 'RU-AMU':'Амурская область', 'RU-ARK':'Архангельская область', 'RU-AST':'Астраханская область', 'RU-BA':'Башкортостан', 'RU-BEL':'Белгородская область', 'RU-BRY':'Брянская область', 'RU-BU':'Бурятия', 'RU-CE':'Чечня', 'RU-CHE':'Челябинская область', 'RU-CU':'Чувашия', 'RU-DA':'Дагестан', 'RU-IN':'Ингушетия', 'RU-IRK':'	Иркутская область', 'RU-IVA':'Ивановская область', 'RU-KAM':'Камчатский край', 'RU-KB':'Кабардино-Балкария', 'RU-KC':'Карачаево-Черкесия', 'RU-KDA':'Краснодарский край', 'RU-KEM':'Кемеровская область', 'RU-KGD':'Калининградская область', 'RU-KGN':'Курганская область', 'RU-KHA':'Хабаровский край', 'RU-KHM':'Ханты-Мансийский автономный округ', 'RU-KIR':'Кировская область', 'RU-KK':'Хакасия', 'RU-KL':'Калмыкия', 'RU-KLU':'Калужская область', 'RU-KO':'Республика Коми', 'RU-KOS':'Костромская область', 'RU-KR':'Республика Карелия', 'RU-KRS':'Курская область', 'RU-KYA':'Красноярский край', 'RU-LIP':'Липецкая область', 'RU-MAG':'Магаданская область', 'RU-ME':'Марий Эл', 'RU-MO':'Мордовия', 'RU-MOW':'Москва', 'RU-MUR':'Мурманская область', 'RU-NGR':'Новгородская область', 'RU-NIZ':'Нижегородская область', 'RU-NVS':'Новосибирская область', 'RU-OMS':'Омская область', 'RU-ORE':'Оренбургская область', 'RU-ORL':'Орловская область', 'RU-PER':'Пермский край', 'RU-PNZ':'Пензенская область', 'RU-PRI':'Приморский край', 'RU-PSK':'Псковская область', 'RU-ROS':'Ростовская область', 'RU-RYA':'Рязанская область', 'RU-SA':'Якутия', 'RU-SAK':'Сахалинская область', 'RU-SAM':'Самарская область', 'RU-SAR':'Саратовская область', 'RU-SE':'Северная Осетия', 'RU-SMO':'Смоленская область', 'RU-SPE':'Санкт-Петербург', 'RU-STA':'Ставропольский край', 'RU-SVE':'Свердловская область', 'RU-TA':'Татарстан', 'RU-TAM':'Тамбовская область', 'RU-TOM':'Томская область', 'RU-TUL':'Тульская область', 'RU-TVE':'Тверская область', 'RU-TY':'Тыва', 'RU-TYU':'Тюменская область', 'RU-UD':'Удмуртия', 'RU-ULY':'Ульяновская область', 'RU-VGG':'Волгоградская область', 'RU-VLA':'Владимирская область', 'RU-VLG':'Вологодская область', 'RU-VOR':'Воронежская область', 'RU-YAN':'Ямало-Ненецкий автономный округ', 'RU-YAR':'Ярославская область', 'RU-YEV':'Еврейская автономная область', 'RU-ZAB':'Забайкальский край'}
    for city in cities.keys():
        offset = 0
        loop = tqdm(total=count_of_pages, position=0, leave=False)

        for i in range(count_of_pages):
                try:
                    loop.set_description('Loading...'.format(i))
                    loop.update(1)

                    response = requests.get(
                        f'https://api.detmir.ru/v2/products?filter=categories[].alias:lego;promo:false;withregion:{city}&expand=meta.facet.ages.adults,meta.facet.gender.adults,webp&meta=*&limit=30&offset={offset}&sort=popularity:desc',
                        cookies=cookies_and_header.cookies, headers=cookies_and_header.headers).json()

                    products_ids = response.get('items')
                    try:
                        for product in products_ids:
                            product_id = product.get('id')
                            article = product.get('article')
                            region_count = len(product.get('available')['offline']['stores'])
                            print(product)
                            if (product_id, article) in cards:
                                cards[(product_id, article)][cities[city]] = region_count

                            else:
                                cards[(product_id, article)] = {cities[city]: region_count}

                        offset += 30
                    except:
                        break
                except ConnectionError:
                    print(f"error in offset {offset}")
        print(cities[city], 'завершено')
    return cards

def toEcxel(cards):
    allData = []
    for k in cards:
        data = {}
        data['ID'] = k[0]
        data['Артикул'] = k[1]
        for r in cards[k]:
            data[r] = cards[k][r]
        allData.append(data)

    df = pd.DataFrame(allData)
    '''
    df.to_excel("alldata.xlsx")'''
    print('Записано в Excel')

if __name__ == "__main__":
    results = get_data()
    toEcxel(results)