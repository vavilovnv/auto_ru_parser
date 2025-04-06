"""Parse and process data from the server."""

from bs4 import BeautifulSoup
from requests import Response, get

from settings import app_settings
from src import strings
from src.schemas import Car


def get_pages_amount(content: bytes) -> int:
    """Calculate number of pages."""
    soup = BeautifulSoup(content, "html.parser")
    target_data = soup.find(strings.SPAN_TAG, class_=strings.TARGET_CLASS)

    if not target_data:
        return 0

    return len(target_data.contents)


def parse_content(*, content: bytes) -> list[Car]:
    """Parsing page content."""
    cars: list[Car] = []

    soup = BeautifulSoup(content, "html.parser")
    items = soup.find_all(strings.DIV_TAG, class_="ListingItem__description")

    for item in items:
        car_data = ""
        if car_content := item.find(strings.DIV_TAG, strings.ITEM_SUMMARY):
            car_data = car_content.get_text()

        url = item.find(strings.A_TAG, strings.ITEM_TITLE_LINK).get(
            strings.HREF_TAG, ""
        )

        car_price = 0
        if price_content := item.find(strings.DIV_TAG, strings.ITEM_PRICE_CONTENT):
            raw_price = price_content.get_text()
            price_data = raw_price.replace(strings.NBSP_CODE, "").split(strings.RUR)
            if len(price_data):
                try:
                    car_price = int(price_data[0])
                except ValueError:
                    car_price = 0

        prod_year = 0
        if year_data := item.find(strings.DIV_TAG, strings.ITEM_YEAR):
            try:
                prod_year = int(year_data.get_text())
            except ValueError:
                prod_year = 0

        cars.append(
            Car(
                description=car_data,
                url=url,
                price=car_price,
                year=prod_year,
            )
        )

    return cars


def get_html(url: str, headers: dict, params: dict | None = None) -> Response:
    """Get the response from the server."""
    try:
        return get(url, headers=headers, params=params)
    except Exception as error:
        raise ConnectionError(f"При выполнении запроса произошла ошибка: {error}")


def parse_response(url: str) -> list[Car] | None:
    """Parse the request."""
    url = url or app_settings.URL
    html = get_html(url, app_settings.HEADERS)
    if html.status_code != 200:
        print(f"Сайт вернул статус-код {html.status_code}")
        return None

    cars: list[Car] = []
    pages_amount = get_pages_amount(html.content)
    for page in range(1, pages_amount + 1):
        print(f"Парсим {page} страницу из {pages_amount}...")

        html = get_html(url, app_settings.HEADERS, params={"page": page})
        cars.extend(parse_content(content=html.content))

    print(f"Получены данные по {len(cars)} авто.")

    return sorted(cars, key=lambda car: int(car.price), reverse=True)
