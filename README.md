# Парсер auto.ru

Простой парсер для выборки данных по авто: данные по автомобилю, ссылка на страницу, стоимость в рублях, год выпуска.
Обработанные данные экспортируются в csv-файл.

Важно заполнить значения `HEADERS`, в частности указать сookie для сайта, который парсится. Иначе может сработать защита 
от ботов. Cookie можно взять в headers страницы с данными по авто, открыв её в инструментах разработчика (chrome) или аналогичной опции в 
другом браузере. 

Установка и запуск:

1. Установить менеджер пакетов [uv](https://pypi.org/project/uv/):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
2. Установить зависимости:
```bash
uv sync
```
3. На базе файла `.env_example` создать файл `.env` и заполнить значения переменных
4. Запустить `main.py`
```bash
uv run main.py
```
5. Ввести url с `auto.ru` с отбором по нужной марке авто
6. Сsv-файл с данными создается в папке указанной в сеттингах проекта. Файл создается текущей датой и временем. Если значение переменной `OPEN_CSV_FILE` равно `True`, то файл будет открыт автоматически после его формирования.

A simple parser to collect cars data: `car`, `url`, `price (RUR)`, `year`. The processed data are exported to a csv file.

![Python](https://img.shields.io/badge/-Python-blue) ![Visitor Badge](https://visitor-badge.laobi.icu/badge?page_id=vavilovnv.Auto_ru)