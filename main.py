import requests
import spark_parse

# TODO неуверенный поиск
# https://spark-interfax.ru/system/sapi/companylist/search?&pageSize=30&pageNo=1&query=
# {"Unknown":"сбер"}&type=Unknown&filter={Country:RUS,OkvedCodes:[],CompanySize:Unknown,RegionCodes:[],
# IsActual:Any,EntityType:Any}&bounds=&documentType=None&ObjectType=Search

if __name__ == '__main__':
    #example
    a = spark_parse.Spark()
    inn_list = [7710699964, 7707083893, 2310031475, 5036045205, ]
    for inn in inn_list:
        a.company_inn = inn

        print(a.accountant_report())

