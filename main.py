from typing import List
import requests


def load_sites():
    with open('sites.txt') as f:
        return f.read().splitlines()


def crawl(sites: List[str]):
    i = 1
    downloaded_pages = ''
    for site in sites:
        if i > 100:
            print('Загружено 100 страниц')
            break

        try:
            headers = {'Accept-Language': 'en-US,en;q=0.5'}
            response = requests.get(site, headers=headers)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении страницы {site}: {e}")
            continue

        if response.status_code == 200:
            html_content = response.text

            with open(f'downloaded_pages/{i}.txt', 'w', encoding='utf-8') as file:
                file.write(html_content)
                downloaded_pages += f'{i}.txt - {site}\n'
                i += 1
        else:
            print(f"Ошибка при получении страницы {site}. Код состояния: {response.status_code}")

    with open('index.txt', 'w', encoding='utf-8') as file:
        file.write(downloaded_pages)


if __name__ == '__main__':
    sites = load_sites()
    crawl(sites)
