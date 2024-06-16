# utils/data_loader.py

import pandas as pd

# Загрузка наборов данных
ozon_df = pd.read_excel('data/sql_20240614_ozon.xlsx')
samokat_df = pd.read_excel('data/sql_20240614_samokat.xlsx')
vprok_df = pd.read_excel('data/sql_20240614_vprok.xlsx')

# Добавление столбца платформы
ozon_df['platform'] = 'ozon'
samokat_df['platform'] = 'samokat'
vprok_df['platform'] = 'vprok'

# Объединение наборов данных
combined_df = pd.concat([ozon_df, samokat_df, vprok_df])
combined_df['cr.price_with_discount'] = combined_df['cr.price_with_discount'] / 100

# Преобразование 'cr.observed_at' в строку для согласованного сравнения
combined_df['cr.observed_at'] = combined_df['cr.observed_at'].astype(str)

# Удаление пробелов из названий брендов и SKU
combined_df['gb.name'] = combined_df['gb.name'].str.strip()
combined_df['dp.name'] = combined_df['dp.name'].str.strip()