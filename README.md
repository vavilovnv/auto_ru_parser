# Парсер auto.ru

Простой парсер для выборки данных по авто: данные по автомобилю, ссылка на страницу, стоимость в рублях, год выпуска.
Обработанные данные экспортируются в csv-файл.

Важно заполнить значения HEADERS, в частности указать сookie для сайта, который парсится. Иначе может сработать защита 
от ботов. Cookie можно взять в headers страницы, открыв её в инструментах разработчика (chrome) или аналогичной опции в 
другом браузере. 

A simple parser to collect cars data: car, url, price (RUR), year. The processed data are exported to a csv file.

![Python](https://img.shields.io/badge/-Python-blue) ![Visitor Badge](https://visitor-badge.laobi.icu/badge?page_id=vavilovnv.Auto_ru)