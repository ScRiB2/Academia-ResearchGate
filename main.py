import csv

import academia
import research_gate

_PATH_TO_FILE = 'C:\\info.csv'
_PATH_TO_DRIVER = 'C:\\Users\\ScRiB\\Desktop\\GChrome\\chromedriver.exe'


def save_in_file(info):
    with open(_PATH_TO_FILE, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, info.keys(), delimiter=';')
        w.writerow(info)


def clear_file():
    f = open(_PATH_TO_FILE, 'w')
    f.close()


if __name__ == '__main__':
    clear_file()
    query = input('Введите запрос: ')
    page_number = input('Введите максимальное количество страниц, которые нужно обработать на сайте ResearchGate: ')
    count_1 = academia.start(query, save_in_file)
    print('\n')
    count_2 = research_gate.start(query, page_number, _PATH_TO_DRIVER, save_in_file)
    print('Всего публикаций получено: ' + str(count_1 + count_2))
    print('Работа программы успешно завершена')
