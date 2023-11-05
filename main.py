from classes import SuperJob, Connector

# def main():
if __name__ == '__main__':
    # main()
    vacancies_json = []
    # keyword = input("Введите вакансию для поиска: ")
    keyword = "Python"

    sj = SuperJob(keyword)
    # sj.get_vacancies(pages_count=2)


    # for api in (sj):
    sj.get_vacancies(pages_count=2)
    vacancies_json.extend(sj.get_formatted_vacancies())

connector = Connector(keyword=keyword)
connector.insert(vacancies_json)


    

# if __name__ == '__main__':
#     main()



