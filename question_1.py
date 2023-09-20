import sqlite3 as sq

with sq.connect('data.db') as con:
    cur = con.cursor()
    
    cur.execute("""SELECT ROUND(SUM("sum"),2)
                    FROM profit
                    WHERE (month == 'июль') AND (status != 'ПРОСРОЧЕНО')
    """)

    result = cur.fetchall()
    print ('----------------------------------------------------------------------------')
    print('Общая выручка за Июль 2021 года, по непросроченным сделкам: ', result[0][0])
    print ('----------------------------------------------------------------------------')