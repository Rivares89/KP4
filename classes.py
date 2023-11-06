import json
from abc import ABC, abstractmethod
from exception import ParsingError
import os
# from dotenv import load_dotenv
import requests
# load_dotenv()
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
            "count": 20,
            "per_page": None,
            "keyword": keyword,
            "archive": False
        }
        self.vacancies = []

    def get_request(self):
        response = requests.get(f'{self.url}/vacancies', params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус: {response.status_code}")
        return response.json()


    def get_vacancies(self, pages_count=1):
        self.vacancies = [] # очищаем список
        for page in range(pages_count):
            page_vacancies = []
            self.params["per_page"] = page
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                # print(json.dumps(page_vacancies, indent=2, ensure_ascii=False))
                self.vacancies.extend(page_vacancies)
                # print(json.dumps(self.vacancies, indent=2, ensure_ascii=False))
                print(f"Загружено вакансий {len(page_vacancies)}")
                print(len(self.vacancies))
                print(self.vacancies)
                # print(json.dumps(self.vacancies, indent=2, ensure_ascii=False))
                # print(page_vacancies)
            if len(page_vacancies) == 0:
                break

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        for vacancy in self.vacancies:
            print(self.vacancies)
            print(json.dumps(vacancy, indent=2, ensure_ascii=False))
            print(f"New")
            formatted_vacancy = {
                "ist": "hh.ru",
                # "employer": vacancy['items'][0]['department'],
                # "title": vacancy['items'][0]['name'],
                # "payment_from": vacancy['items'][0]['salary']['from'],
                # "payment_to": vacancy['items'][0]['salary']['to'],
            }
            formatted_vacancies.append(formatted_vacancy)
        return formatted_vacancies

class SuperJob(Engine):
    url = "	https://api.superjob.ru/2.0/vacancies/"

    def __init__(self, keyword):
        self.params = {
            "count": 100,
            "page": None,
            "keyword": keyword,
            "archive": False
        }

        self.headers = {
            "X-Api-App-Id": "v3.r.137936779.c561df967b4d14c5d30f8b6e3132e9b7bc52cb7f.e8b0c26ac031c925476eba981ecfa9c3dcd8a66f"

        }
        self.vacancies = []

    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус: {response.status_code}")
        return response.json()["objects"]


    def get_vacancies(self, pages_count=2):

        self.vacancies = [] # очищаем список
        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)

                print(f"Загружено вакансий {len(self.vacancies)}")

            if len(page_vacancies) == 0:
                break

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        for vacancy in self.vacancies:
            formatted_vacancy = {
                "employer": vacancy["firm_name"],
                "title": vacancy["profession"],
                "payment_from": vacancy["payment_from"],
                "payment_to": vacancy["payment_to"],
            }
            formatted_vacancies.append(formatted_vacancy)
        return formatted_vacancies

class Vacancy:
    def __init__(self, vacancy):
        self.employer = vacancy.employer
        self.title = vacancy.title
        self.payment_from = vacancy.payment_from
        self.payment_to = vacancy.payment_to


class Connector:
    def __init__(self, keyword):
        self.filename = f"{keyword.title()}.json"

    def insert(self, vacancies_json):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(vacancies_json, file, indent=4, ensure_ascii=False)

    def select(self):

        with open(self.filename, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
        return [Vacancy(x) for x in vacancies]
        pass
