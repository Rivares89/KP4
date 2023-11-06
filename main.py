from classes import SuperJob, Connector, HeadHunter

# def main():
if __name__ == '__main__':
    vacancies_json = []
    keyword = "Python"

    sj = SuperJob(keyword)

    sj.get_vacancies(pages_count=1)
    vacancies_json.extend(sj.get_formatted_vacancies())

    connector = Connector(keyword=keyword)
    connector.insert(vacancies_json)

    hh = HeadHunter(keyword)
    hh.get_vacancies(pages_count=2)
    vacancies_json.extend(hh.get_formatted_vacancies())

    connector = Connector(keyword=keyword)
    connector.insert(vacancies_json)

# if __name__ == '__main__':
#     main()