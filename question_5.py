import sqlite3 as sq

with sq.connect('data.db') as con:
    cur = con.cursor()

    cur.execute("""SELECT COUNT(document)
                    FROM profit
                    WHERE (document == 'оригинал') AND (month == 'май') AND (receiving_date LIKE '%2021-06-%')
    """)

    result = cur.fetchall()
    print('-----------------------------------------------------------------------------------------')
    print('Количество оригиналов договора по майским сделкам, которые были получены в Июне: ', result[0][0])
    print('-----------------------------------------------------------------------------------------')