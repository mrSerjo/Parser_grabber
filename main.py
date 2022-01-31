import requests
from bs4 import BeautifulSoup
from decouple import config
import time
from random import randrange


headers = {
    'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': config('USER_AGENT'),
}


def get_articles_urls(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')
    pagination_count = int(soup.find(
        'span', class_='navigations').find_all('a')[-1].text)

    articles_urls_list = []
    for page in range(1, pagination_count + 1):
        response = s.get(url=f'https://hi-tech.news/page/{page}/',
                         headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        articles_urls = soup.find_all('a', class_='post-title-a')

        for au in articles_urls:
            art_url = au.get('href')
            articles_urls_list.append(art_url)

        time.sleep(randrange(2, 5))  # Бездействие, чтобы сайт не забанил или не вывел капчу для подтверждения
        print(f'Обработал {page}/{pagination_count}')

    with open('aritcles_urls.txt', 'w') as file:
        for url in articles_urls_list:
            file.write(f'{url}\n')

    return 'Работа по сбору ссылок выполнена'


def main():
    print(get_articles_urls(url='https://hi-tech.news/'))


if __name__ == '__main__':
    main()