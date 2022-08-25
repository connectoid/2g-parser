import csv
from urllib import response
import requests
from bs4 import BeautifulSoup
from xlsxwriter.workbook import Workbook
import glob
import os
import time
import random

min_url = 'https://2gis.ru'
base_url = 'https://2gis.ru/search/'
search_url = 'Тульская область автозапчасти'
OUTPUT_FILE = 'out.csv'
filename = 'out.csv'
delay_range_urls = 5
delay_range_firms = 10

main_url = base_url + search_url
UA = 'Out: ''Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.37 (KHTML, like Gecko) Chrome/41.0.2224.5 Safari/537.39'
header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
        'referer':'https://www.google.com/'
    }
test_urls = [
    'https://2gis.ru/p_kamchatskiy/firm/5067078862413191',
    'https://2gis.ru/p_kamchatskiy/firm/5067078862103744',
    'https://2gis.ru/p_kamchatskiy/firm/70000001059933705',
    'https://2gis.ru/p_kamchatskiy/firm/5067078862343918']

test_url = 'https://2gis.ru/tula/firm/5067078862413191'
socials = ['WhatsApp', 'Telegram', 'ВКонтакте', 'Viber', 'Одноклассники']

def save_data(data):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, dialect='excel', delimiter = ",")
        writer.writerow(['Наименование', 'Адрес','Координаты','Телефоны','Адрес сайта'])
        for item in data:
            writer.writerow(item)

def get_company_data(url):
    try:
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.text, 'lxml')
    except Exception as error:
        print('Возникла ошибка: ', error)
        soup = None
    return soup


def get_phone(phone_string):
    if phone_string:
        return phone_string.find('a')
    else:
        return ''

def get_site(site_string):
    site = ''
    if site_string:
        try:
            site = site_string.find_all('a', class_='_1rehek')[1].text
        except KeyError as error:
            print('get site error ', error)
            return ''
        finally:
            return site
    else:
        return ''

def get_address(region, street):
    address = ''
    if region:
        region = region.text.strip() + ', '
    else:
        region = ''
    if street:
        street = street.text.strip().replace(u'\xa0', u' ').replace(u'\u200b', u'')
    else:
        street = ''
    address = region + street
    return address
    
    region.text.strip() + ', ' + street.text.strip().replace(u'\xa0', u' ').replace(u'\u200b', u'')

def parse_company_data(soup):
    data = []
    if soup:
        name, description, region = '', '', ''
        name = soup.find('span', class_='_oqoid')
        description = soup.find('article', class_='_xhakwn')
        region = soup.find('div', class_='_1p8iqzw')
        street = soup.find('span', class_='_er2xx9')
        phone = soup.find('div', class_='_b0ke8')
        site = soup.find('div', class_='_t0tx82')
        geo = soup.find('span', class_='_er2xx9')
        
        if name:
            name = name.text.strip()
            print(f'Добавлена фирма {name}')
            data.append(name)
        else:
            print('Фирма пропущена')
        data.append(get_address(region, street))
        if geo:
            data.append(min_url + geo.find('a')['href'])
        if phone:
            try:
                data.append(get_phone(phone)['href'])
            except KeyError as error:
                print('### error: ', error)
        if site:
            try:
                site = get_site(site)
            except KeyError as error:
                print('### error: ', error)
            finally:
                if site and site not in socials:
                    data.append('http://' + site)
                else:
                    data.append('')
        if description:
            data.append(description.text.strip())
        else:
            data.append('')
    return data

def get_urls_data(url, page):
    url = url + '/page/' + str(page)
    print('Обрабатываем страницу ', url)
    delay = random.randint(1, delay_range_urls)
    print(f'Делаем задержку {delay} сек')
    time.sleep(delay)
    try:
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.text, 'lxml')
    except Exception as error:
        print('Возникла ошибка: ', error)
        soup = None
    return soup

def get_companies_list(soup):
    if soup:
        list = soup.find_all('div', class_='_1h3cgic')
        cleared_urls = []
        for item in list:
            cleared_urls.append(min_url + item.find('a', class_='_1rehek')['href'])
    else:
        print('Произошла ошибка, попробуйте позже')
    if cleared_urls:
        return cleared_urls
    else:
        return None

def get_all_urls(count):
    main_list = []
    for page in range(1, count + 1):
        data = get_urls_data(main_url, page)
        companies_list = get_companies_list(data)
        if companies_list:
            for company_url in companies_list:
                main_list.append(company_url)
        else:
            print(f'Страница номер {page} пустая')
    return main_list

def save_in_xlsx(csvfile):
    for csvfile in glob.glob(os.path.join('.', '*.csv')):
        workbook = Workbook(csvfile[:-4] + '.xlsx')
        worksheet = workbook.add_worksheet()
        with open(csvfile, 'rt', encoding='utf8') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)
        workbook.close()

def main():
    f = open(filename, 'w')
    f.close()
    main_list = get_all_urls(2)
    companies_data = []
    for url in main_list:
        delay = random.randint(1, delay_range_firms)
        soup = get_company_data(url)
        print(f'Делаем задержку {delay} сек')
        time.sleep(delay)
        if soup:
            data = parse_company_data(soup)
            companies_data.append(data)
        else:
            print('No soup')
    save_data(companies_data)
    save_in_xlsx(filename)

if __name__ == '__main__':
    main()