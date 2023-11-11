from classes import SuperJob, Connector, HeadHunter

# def main():
if __name__ == '__main__':
    vacancies_json = []
    keyword = "Python"

    hh = HeadHunter(keyword)
    sj = SuperJob(keyword)

    for api in (hh, sj):
        api.get_vacancies(pages_count=3)
        vacancies_json.extend(api.get_formatted_vacancies())


    # sj.get_vacancies(pages_count=1)
    # vacancies_json.extend(sj.get_formatted_vacancies())
    #
    # connector = Connector(keyword=keyword)
    # connector.insert(vacancies_json)
    #
    #
    # hh.get_vacancies(pages_count=1)
    # vacancies_json.extend(hh.get_formatted_vacancies())

    connector = Connector(keyword=keyword)
    connector.insert(vacancies_json)

# if __name__ == '__main__':
#     main()