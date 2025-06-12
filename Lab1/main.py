import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

def parse_vacancies(url, pages=3):
    headers = {'User-Agent': 'Mozilla/5.0'}
    vacancies = []

    for page in range(pages):
        params = {'page': page}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        vacancy_cards = soup.select('div.vacancy-card--n77Dj8TY8VIUF0yM')
        if not vacancy_cards:
            break

        for card in vacancy_cards:
            title_tag = card.select_one('span.vacancy-name-wrapper--PSD41i3dJDUNb5Tr a')
            title = title_tag.text.strip() if title_tag else ''
            link = title_tag['href'] if title_tag and title_tag.has_attr('href') else ''

            salary_tag = card.select_one('div.compensation-labels--vwum2s12fQUurc2J')
            salary = salary_tag.text.strip() if salary_tag else 'Не указана'

            address_tag = card.select_one('span[data-qa="vacancy-serp__vacancy-address"]')
            address = address_tag.text.strip() if address_tag else ''

            vacancies.append({
                'Название': title,
                'Зарплата': salary,
                'Адрес': address,
                'Ссылка': link
            })

    return vacancies

def save_to_excel(vacancies, filename='vacancies.xlsx'):
    wb = Workbook()
    ws = wb.active
    ws.title = "Вакансии hh.ru"
    headers = ['Название', 'Зарплата', 'Адрес', 'Ссылка']
    ws.append(headers)

    for vac in vacancies:
        ws.append([vac[h] for h in headers])

    wb.save(filename)
    print(f'Данные сохранены в файл {filename}')

if __name__ == '__main__':
    url = 'https://omsk.hh.ru/search/vacancy?text=Python&salary=&ored_clusters=true&order_by=publication_time&area=68&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line'
    vacancies = parse_vacancies(url, pages=1)
    save_to_excel(vacancies)
