import sqlite3 as sq
import matplotlib.pyplot as plt

with sq.connect('data.db') as con:
    cur = con.cursor()

    cur.execute("""SELECT month, ROUND(SUM("sum"),2)
                    FROM profit
                    WHERE status != 'ПРОСРОЧЕНО'
                    GROUP BY month
                    ORDER BY
                    CASE
                        WHEN month = 'май' THEN 1
                        WHEN month = 'июнь' THEN 2
                        WHEN month = 'июль' THEN 3
                        WHEN month = 'август' THEN 4
                        WHEN month = 'сентябрь' THEN 5
                        WHEN month = 'октябрь' THEN 6
                    END;
    """)

    result = cur.fetchall()

        #Вывод графика 
    months = [item[0] for item in result]
    sums = [item[1] for item in result]
    plt.plot(months, sums, marker='o', linestyle='-')
    plt.xlabel('Месяц')
    plt.ylabel('Сумма')
    plt.title('Изменение выручки за текущий период')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()