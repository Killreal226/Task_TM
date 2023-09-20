import sqlite3 as sq

with sq.connect('data.db') as con:
    cur = con.cursor()

    cur.execute("""SELECT sale, ROUND(SUM("sum"),2) AS total_sum
                    FROM profit
                    WHERE (status != 'ПРОСРОЧЕНО') AND (month == 'сентябрь')
                    GROUP BY sale
                    ORDER BY total_sum DESC;
    """)

    result = cur.fetchall()
    print('--------------------------------------------------------------------------------------')
    print('Менеджер, привлекший для компании больше всего денежных средств в сентябре: ', result[0][0])
    print('--------------------------------------------------------------------------------------')