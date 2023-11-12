# импорт библиотек
import json
from abc import ABC, abstractmethod
from datetime import datetime
from config import API_KEY
from exception import ParsingError
import requests

class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

class HeadHunter(Engine):
    url = "https://api.hh.ru"

    def __init__(self, keyword):
        self.params = {
            "text": keyword,
            "page": None,
            "per_page": 5
        }
        self.vacancies = []

    def get_request(self):
        '''Делает запрос и возвращает в формате json'''
        response = requests.get(f'{self.url}/vacancies', params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус: {response.status_code}")
        return response.json()


    def get_vacancies(self, pages_count=10):
        '''Проходим циклом по словарю  записываем данные в переменную "vacancies" '''
        self.vacancies = [] # очищаем список
        for page in range(pages_count):
            page_vacancies = []
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies['items'])
                print(f"Загружено вакансий {len(page_vacancies['items'])}")
            if len(page_vacancies) == 0:
                break

    def get_formatted_vacancies(self):
        '''Проходим циклом по данным, записанным в self.vacancies и берем только нужные нам данные и записываем в formatted_vacancies'''
        formatted_vacancies = []
        for vacancy in self.vacancies:
            published_at = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z")
            formatted_vacancy = {
                "employer": vacancy['department']['name'] if vacancy.get('department') else None,
                "title": vacancy['name'],
                "payment_from": vacancy['salary']['from'] if vacancy.get('salary') else None,
                "payment_to": vacancy['salary']['to'] if vacancy.get('salary') else None,
                'responsibility': vacancy['snippet']['responsibility'],
                'link': vacancy['apply_alternate_url'],
                'date': published_at.strftime("%d.%m.%Y"),
            }
            formatted_vacancies.append(formatted_vacancy)
        return formatted_vacancies

class SuperJob(Engine):
    url = "	https://api.superjob.ru/2.0/vacancies/"

    def __init__(self, keyword):
        self.params = {
            "count": 2,
            "page": None,
            "keyword": keyword,
            "archive": False
        }
        self.headers = {
            "X-Api-App-Id": API_KEY
        }
        self.vacancies = []

    def get_request(self):
        '''Делает запрос по API и возвращает в формате json'''
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус: {response.status_code}")
        return response.json()["objects"]


    def get_vacancies(self, pages_count=2):
        '''Проходим циклом по словарю  записываем данные в переменную "vacancies" '''
        self.vacancies = [] # очищаем список
        for page in range(pages_count):
            page_vacancies = []
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                print(f"Загружено вакансий {len(page_vacancies)}")
            if len(page_vacancies) == 0:
                break

    def get_formatted_vacancies(self):
        '''Проходим циклом по данным, записанным в self.vacancies и берем только нужные нам данные и записываем в formatted_vacancies'''
        formatted_vacancies = []
        for vacancy in self.vacancies:
            published_at = datetime.fromtimestamp(vacancy.get('date_published', ''))
            formatted_vacancy = {
                "employer": vacancy["firm_name"],
                "title": vacancy["profession"],
                "payment_from": vacancy["payment_from"],
                "payment_to": vacancy["payment_to"],
                'responsibility': vacancy.get('candidat').replace('\n', '').replace('•', '') if vacancy.get('candidat') else None,
                'link': vacancy['client']['link'],
                'date': published_at.strftime("%d.%m.%Y"),
            }
            formatted_vacancies.append(formatted_vacancy)
        return formatted_vacancies

class Vacancy:
    def __init__(self, vacancy):
        self.employer = vacancy["employer"]
        self.title = vacancy["title"]
        self.payment_from = vacancy['payment_from'] if vacancy['payment_from'] else 0
        self.payment_to = vacancy['payment_to'] if vacancy['payment_to'] else 0
        self.responsibility = vacancy['responsibility']
        self.link = vacancy['link']
        self.date = vacancy['date']

    def __str__(self):
        '''Показывает информацию об объекте класса'''
        output_str = f"""
        employer = {self.employer}
        title = {self.title}
        payment_from = {self.payment_from}
        payment_to = {self.payment_to}
        responsibility = {self.responsibility}
        link = {self.link}
        date = {self.date}
"""
        return output_str

    # Магические методы для сравнения по payment_from
    def __gt__(self, other):
        return self.payment_from > other.payment_from

    def __ge__(self, other):
        return self.payment_from >= other.payment_from

    def __lt__(self, other):
        return self.payment_from < other.payment_from

    def __le__(self, other):
        return self.payment_from <= other.payment_from

class Connector:
    def __init__(self, keyword):
        self.filename = f"data/{keyword.lower()}.json"

    def insert(self, vacancies_json):
        '''Запись в файл'''
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(vacancies_json, file, indent=4, ensure_ascii=False)

    def select(self):
        '''Возвращает список объектов класса Vacancy'''
        with open(self.filename, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
        return [Vacancy(x) for x in vacancies]

    def sort_vacancy(self):
        '''Сортировка при помощи магических методов сравнения по ключу "payment_from" '''
        vacancies = self.select()
        return sorted(vacancies)

    def sort_vacancy_payment_to(self):
        '''Сортировка вакансий по ключу "payment_to" '''
        vacancies = self.select()
        return sorted(vacancies, key=lambda x: x.payment_to)
