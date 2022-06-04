import csv
import os

from requests import get
from bs4 import BeautifulSoup


PATH = 'Cars.csv'
URL = 'https://auto.ru/moskva/cars/bmw/x3/21029610/all/engine-dizel/?displacement_from=2000&displacement_to=2000'
COOKIE = 'gdpr=0; _ym_uid=1619278461997459506; _ym_visorc=b; _ym_isad=1; spravka=dD0xNjU0Mjc3NzcyO2k9NDYuMjQyLjE1LjE5MztEPUVBRTUwNUFGODU0NEM1RTgzQ0U0REEzMjNFMkUzOTJDRjJFMUNFNDQwRkYxNDAyNTUzRjkyODhGMjlGQjMzODkyRjRBNEEzRTt1PTE2NTQyNzc3NzIzMjE0MDMwNTE7aD0zOTY3NjM1MDFlNWI2MjNhN2UzNDhiYjhmYmVjM2M3MA==; _csrf_token=1586ebc7d965543cea88980c678c18729a8ee5a4fa25e828; suid=80d4f87575d141e64b4da52c115173bc.a97c3f658ba290f6cc515b8d6cf8916e; from=direct; yuidlt=1; yandexuid=6794932891604144833; my=YwA%3D; ys=wprid.1649078117675326-6625865166469650921-sas3-0671-f04-sas-l7-balancer-8080-BAL-9103%23c_chck.1864184180%23udn.cDpmb3JpZ2I%3D; autoru_sid=a%3Ag629a468c2fdl5ch0m73fl1l2fohbi17.a6b91f18983679341268aaf47534c357%7C1654277772749.604800.1EgAMCF7bdH0WgL2t1OlRw.rWA5lbbL9Djq8ryfMWKzwp4GsFhA-JE_JhF-N-gYZBo; autoruuid=g629a468c2fdl5ch0m73fl1l2fohbi17.a6b91f18983679341268aaf47534c357; crookie=x/zT0vfhfWgKBRS81y+PmO6EH0QS3y58a/PQnxnPv4oaKA34zaT34doBkPOOBZQK/43iNv28/LWHpdautd2CeW4RRbI=; cmtchd=MTY1NDI3Nzc3MzcwNQ==; Session_id=3:1654277778.5.0.1653314975149:wQ_yLg:1b.1.2:1|21159945.0.2|61:4922.685882.Nzy1wUIiUzNsGhiBfmIB_BtRUAE; yandex_login=forigb; i=wdqo4jvrMavcxNfyb4zMjCyTSF9p+HmsT3zHsbmTj6ula6FBIyyFIv7DMbQBe39KFnSpHarT7oDdydq3txWIAmROmLw=; mda2_beacon=1654277778616; sso_status=sso.passport.yandex.ru:blocked; _yasc=PGxPIjCIIEuLS5l4cShGktY8QdRHcGA7/zJ4Ps1V5YMopxw3; los=1; bltsr=1; from_lifetime=1654278053031; _ym_d=1654278079'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru',
    'accept-encoding': 'accept - encoding: gzip, deflate, br',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Opera";v="87"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'Cookie': COOKIE
}


def get_pages_amount(html):
    soup = BeautifulSoup(html, 'html.parser')
    return len(soup.find(
        'span',
        class_='ControlGroup ControlGroup_responsive_no ControlGroup_size_s ListingPagination__pages'
    ).contents)


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='ListingItem__description')
    cars = []
    for item in items:
        car = {
            'car': item.find('div', 'ListingItem__summary').get_text(),
            'url': item.find('a', 'Link ListingItemTitle__link').get('href'),
            'price': item.find('div', 'ListingItemPrice__content').get_text().replace(' ', '').replace('₽', ''),
            'year': item.find('div', 'ListingItem__yearBlock').get_text(),
        }
        cars.append(car)
    return cars


def get_html(url, headers, params=None):
    return get(url, headers=headers, params=params)


def parse(url=URL):
    html = get_html(url, HEADERS)
    if html.status_code == 200:
        cars = []
        pages_amount = get_pages_amount(html.content)
        for i in range(1, pages_amount + 1):
            print(f'Парсим {i} страницу из {pages_amount}...')
            html = get_html(url, HEADERS, params={'page': i})
            cars.extend(get_content(html.content))
        print(f'Получены данные по {len(cars)} авто.')
        return sorted(cars, key=lambda car: int(car['year']), reverse=True)
    else:
        print(f'Сайт вернул статус-код {html.status_code}')


def save_to_file(data):
    with open(PATH, 'w', newline='', encoding='utf-8') as file:
        w = csv.writer(file, delimiter=';')
        w.writerow(['Car', 'Link', 'Price (RUR)', 'Year'])
        for car in data:
            w.writerow([
                car['car'],
                car['url'],
                car['price'],
                car['year']
            ])
        os.startfile(PATH)


def main():
    data = parse(input('URL: ').strip())
    if len(data) > 0:
        save_to_file(data)


if __name__ == '__main__':
    main()
