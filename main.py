
import requests
from bs4 import BeautifulSoup
import json
import os
import argparse


def get_html(url):                                                          # запрос на сервер и получение ответа в html
    req = requests.get(url)
    return req.text


def save_json(path_='', filename='data_file.json'):
    full_file_name = os.path.join(path_, file_name)
    with open(file_name, "w", encoding='UTF-8') as file:                       # создание json в папке исходника
        json.dump(data, file, indent=2, ensure_ascii=False)


def write_json(data):                                                             # создание пути сохранения и файл json
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--path', type=str, help='Укажите путь')
        args = parser.parse_args()
        path_ = args.path
        if path_ is None:
            save_json()
        else:
            if not os.path.exists(path_):                                          # Если пути не существует создаем его
                os.makedirs(path_)
                save_json(path_=path_)
             
    except FileNotFoundError:
        print('try -h, --help')


def get_data(html):                                                       # сам парсинг и создание словаря с результатом

    data = BeautifulSoup(html, 'lxml')

    tr_data = data.find('table', class_='data').find('tbody').find_all('tr')
    date = data.find('div', class_='datepicker-filter').find('button', class_='datepicker-filter_button').text

    dict_ = {'Date': date}

    for tr in tr_data:
        td_data = tr.find_all('td')
        if len(td_data) != 0:
            num_code = td_data[0].text
            char_code = td_data[1].text
            unit = td_data[2].text
            currency = td_data[3].text
            rate = td_data[4].text
            """Создаем словарь с данными с сайты"""
            data = {
                char_code: {
                    'Цифр. код': num_code,
                    'Единица': unit,
                    'Валюта': currency,
                    'Курс': rate
                    }
                }
            dict_.update(data)

    write_json(dict_)


def main():                                                                              # адрес сервера, вызов функиций
    url = 'https://www.cbr.ru/currency_base/daily/'
    get_data(get_html(url))


if __name__ == '__main__':
    main()
