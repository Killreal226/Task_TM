import sqlite3 as sq

with sq.connect('data.db') as con:
    cur = con.cursor()

    cur.execute("""SELECT "new/current", COUNT("new/current") AS count_deal
                    FROM profit
                    WHERE month == 'октябрь'
                    GROUP BY "new/current"
                    ORDER BY count_deal DESC;
    """)

    result = cur.fetchall()
    print('-----------------------------------------------------')
    print('В октябре преобладал такой тип сделок: ', result[0][0])
    print('-----------------------------------------------------')