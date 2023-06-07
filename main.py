import requests
import  spark_parse









# TODO неуверенный поиск
# https://spark-interfax.ru/system/sapi/companylist/search?&pageSize=30&pageNo=1&query=
# {"Unknown":"сбер"}&type=Unknown&filter={Country:RUS,OkvedCodes:[],CompanySize:Unknown,RegionCodes:[],
# IsActual:Any,EntityType:Any}&bounds=&documentType=None&ObjectType=Search

#
a=spark_parse.Spark()
inn_list=[7710699964,7707083893,2310031475,5036045205,]
for inn in inn_list:
    a.company_inn=inn
#guid= a.get_guid(7710699964)
#print(guid)
    print(a.accountant_report())



#a.company_inn=7707083893
#guid= a.get_guid(7707083893)
#print(guid)
#a.get_company_info()
