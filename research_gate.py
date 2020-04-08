import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

_MAIN_URL = 'https://www.researchgate.net/search/publication?q={0}&page={1}'
_RIS_URL = 'https://www.researchgate.net/publication/{0}/citation/download'


def check_captcha(driver):
    """Проверяем наличие капчи"""
    try:
        driver.find_element_by_id('captcha-form')
        print('Ожидаем ввода капчи')

        try:
            WebDriverWait(driver, 3000).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'search'))
            )
        finally:
            pass
        print('Капча введена успешно')
        return True

    except NoSuchElementException:
        return False


def get_info_from_item(item, save_in_file):
    div = item.find_element_by_class_name('nova-v-publication-item__body')
    divs = div.find_elements_by_class_name('nova-v-publication-item__stack-item')

    length = len(divs)
    index_title = 0
    index_authors = 2
    if length == 4:
        index_title = 1
        index_authors = 3

    a = divs[index_title].find_element_by_tag_name('a')

    title = divs[index_title].text
    href = a.get_attribute('href')
    url = href[0:href.rfind('?')]

    lis = divs[index_authors].find_elements_by_tag_name('li')
    authors = []
    for li in lis:
        authors.append(li.text)
    authors = ' and '.join(authors)
    info = {
        'title': title,
        'authors': authors,
        'url': url
    }
    save_in_file(info)


def start(query, page_number, path_to_driver, save_in_file):
    print('Начинаем работу с сайтом ResearchGate')

    driver = webdriver.Chrome(executable_path=r'{0}'.format(path_to_driver))
    pubs = 0
    i = 1
    while True:
        driver.get(_MAIN_URL.format(query, i))

        check_captcha(driver)

        print('Обрабатываем страницу ' + str(i) + '...')

        time.sleep(3)
        container = driver.find_element_by_class_name('js-items')
        items = container.find_elements_by_class_name('nova-o-stack__item')
        if len(items) == 11:
            items.pop()

        for item in items:
            get_info_from_item(item, save_in_file)
            pubs = pubs + 1

        if len(items) != 10 or i == int(page_number):
            break
        i = i + 1

    print('Публикаций получено: ' + str(pubs))
    print('\n')
    driver.quit()
    return pubs
