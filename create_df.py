import pandas as pd
from sqlalchemy import create_engine

    #Создание pandas DataFrame
df = pd.read_excel('data.xlsx')

    #Предварительное форматирование таблицы
df = df.drop([0,129,258,369,484,594])
df = df.drop(columns=['Unnamed: 5'])

    #Создание нового столбца месяц
df['month'] = 0
df.loc[1:128, 'month'] = 'май'
df.loc[130:257, 'month'] = 'июнь'
df.loc[259:368, 'month'] = 'июль'
df.loc[370:483, 'month'] = 'август'
df.loc[485:593, 'month'] = 'сентябрь'
df.loc[595:, 'month'] = 'октябрь'

    #Запись полученной таблицы в БД
engine = create_engine('sqlite:///data.db')
try:
    df.to_sql('profit', engine, index=False)
except:
    pass

print('End!')
