import spark_parse

if __name__ == '__main__':
    # example
    a = spark_parse.Spark()
    inn_list = [7710699964, 7707083893, 2310031475, 5036045205]
    for inn in inn_list:
        a.company_inn = inn

        print(a.accountant_report())
