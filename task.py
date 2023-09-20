import sqlite3 as sq
from prettytable import PrettyTable

with sq.connect('data.db') as con:
    cur = con.cursor()

        #Создание промежуточных табллиц
            #Таблица бонуса 1
    cur.execute("""CREATE TABLE bonus_1 AS
                    SELECT sale, SUM("sum"*0.07) AS total_sum
                    FROM profit
                    WHERE (status == 'ОПЛАЧЕНО') AND ("new/current" == 'новая')
                    AND (receiving_date NOT LIKE '2021-05-%')
                    AND (receiving_date NOT LIKE '2021-06-%')
                    AND (month NOT IN ('июль', 'август', 'сентябрь', 'октябрь'))
                    GROUP BY sale
    """)
            #Таблица бонуса 2 (5 % от суммы)
    cur.execute("""CREATE TABLE bonus_2_1 AS
                    SELECT sale, SUM("sum"*0.05) AS total_sum
                    FROM profit
                    WHERE (status != 'ПРОСРОЧЕНО') AND ("sum" > 10000) AND ("new/current" == 'текущая') 
                    AND (receiving_date NOT LIKE '2021-05-%')
                    AND (receiving_date NOT LIKE '2021-06-%')
                    AND (month NOT IN ('июль', 'август', 'сентябрь', 'октябрь'))
                    GROUP BY sale
    """)
            #Таблица бонуса 2 (3 % от суммы)
    cur.execute("""CREATE TABLE bonus_2_2 AS
                    SELECT sale, SUM("sum"*0.03) AS total_sum
                    FROM profit
                    WHERE (status != 'ПРОСРОЧЕНО') AND ("sum" <= 10000) AND ("new/current" == 'текущая')
                    AND (receiving_date NOT LIKE '2021-05-%')
                    AND (receiving_date NOT LIKE '2021-06-%')
                    AND (month NOT IN ('июль', 'август', 'сентябрь', 'октябрь'))
                    GROUP BY sale
    """)
            #Таблица всех имен
    cur.execute("""CREATE TABLE names AS
                    SELECT sale 
                    FROM profit
                    GROUP BY sale
    """)          
            #Таблица общего ненулевого бонуса для каждого менеджера
    cur.execute("""CREATE TABLE bonus AS
                SELECT sale, SUM(total_sum) AS total_sum
                FROM (
                SELECT sale, total_sum FROM bonus_1
                UNION ALL
                SELECT sale, total_sum FROM bonus_2_1
                UNION ALL
                SELECT sale, total_sum FROM bonus_2_2
                ) AS combined_data
                GROUP BY sale;
    """)                  
        #Конечный запрос
    cur.execute("""SELECT names.sale, COALESCE(bonus.total_sum, 0) AS total_sum
                    FROM names
                    LEFT JOIN bonus ON names.sale = bonus.sale
                    WHERE bonus.sale IS NULL
                    UNION ALL
                    SELECT sale, ROUND(total_sum, 2)
                    FROM bonus  
                    ORDER BY total_sum DESC;            
    """)

    result = cur.fetchall()
    table = PrettyTable()
    table.field_names = ['ФАМИЛИЯ', 'ОСТАТОК НА ИЮЛЬ']

    for val in result:
        if val[0] == '-':
            continue
        table.add_row([val[0], val[1]])
    print(table)

        #Удаление промежуточных таблиц
    cur.execute("DROP TABLE bonus;")
    cur.execute("DROP TABLE bonus_1;")
    cur.execute("DROP TABLE bonus_2_1;")
    cur.execute("DROP TABLE bonus_2_2;")
    cur.execute("DROP TABLE names;")