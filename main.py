from classes import SuperJob, Connector, HeadHunter, Vacancy

def main():
    vacancies_json = []
    keyword = input("Введите ключевое слово для поиска: ")

    hh = HeadHunter(keyword)
    sj = SuperJob(keyword)

    for api in (hh, sj):
        api.get_vacancies(pages_count=10)
        vacancies_json.extend(api.get_formatted_vacancies())

    connector = Connector(keyword=keyword)
    connector.insert(vacancies_json)

    EXIT = "0"
    SORTED_vacancy = "1"
    SORTED_vacancy_by_payment_from = "2"
    SORTED_vacancy_by_payment_to = "3"
    while True:
        command = input(
            "1 - Вывести список вакансий;\n"
            "2 - Отсортировать по минимальной зарплате 'зарплата от';\n"
            "3 - Отсортировать по минимальной зарплате 'зарплата до';\n"
            "0 - Выход \n"
        )

        if command == EXIT:
            break
        elif command == SORTED_vacancy:
            vacancies = connector.select()
            for vacancy in vacancies:
                print(vacancy)
        elif command == SORTED_vacancy_by_payment_from:
            vacancies = connector.sort_vacancy()
            print(*vacancies, end="\n")
        elif command == SORTED_vacancy_by_payment_to:
            vacancies = connector.sort_vacancy_payment_to()
            print(*vacancies, end="\n")



if __name__ == '__main__':
    main()