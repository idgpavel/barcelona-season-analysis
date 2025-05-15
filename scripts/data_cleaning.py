import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_data(df, output_path='data/processed/matches.csv'):
    try:
        os.makedirs('data/processed', exist_ok=True)
        # Удаление дубликатов
        df = df.drop_duplicates()
        # Удаление пропусков в ключевых столбцах
        key_columns = ['date', 'opponent', 'goals_for', 'goals_against', 'venue', 'result']
        df = df.dropna(subset=key_columns)
        # Форматирование столбцов
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        # Преобразование типов
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['goals_for'] = pd.to_numeric(df['goals_for'], errors='coerce').fillna(0).astype(int)
        df['goals_against'] = pd.to_numeric(df['goals_against'], errors='coerce').fillna(0).astype(int)
        # Добавление matchday
        df['matchday'] = range(1, len(df) + 1)
        # Сохранение
        df.to_csv(output_path, index=False)
        logging.info(f"Очищенные данные сохранены в {output_path}")
        return df
    except Exception as e:
        logging.error(f"Ошибка при очистке данных: {e}")
        return None

def perform_eda(df):
    try:
        print("=== Разведывательный анализ данных (EDA) ===")
        print("\n1. Типы переменных:")
        print(df.dtypes)
        print("\n2. Описательные статистики:")
        print(df.describe(include='all'))
        print("\n3. Количество пропусков:")
        print(df.isnull().sum())
        print("\n4. Уникальные значения:")
        for col in df.select_dtypes(include='object').columns:
            print(f"{col}: {df[col].nunique()} уникальных значений")
        print("\n5. Наиболее частые значения:")
        for col in df.select_dtypes(include='object').columns:
            print(f"{col}:\n{df[col].value_counts().head()}")
    except Exception as e:
        logging.error(f"Ошибка при EDA: {e}")

if __name__ == "__main__":
    try:
        df = pd.read_csv('data/raw/matches.csv')
        df_cleaned = clean_data(df)
        if df_cleaned is not None:
            perform_eda(df_cleaned)
    except FileNotFoundError:
        logging.error("Файл data/raw/matches.csv не найден")
