import streamlit as st
import pandas as pd
import plotly.express as px
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

st.set_page_config(page_title="Анализ Барселоны 2024/2025", layout="wide")

st.title("📊 Анализ сезона ФК Барселона 2024/2025")
st.markdown("Исследование статистики матчей: тренды голов, домашние/гостевые игры, результаты.")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/processed/matches.csv")
        logging.info("Данные успешно загружены")
        return df
    except FileNotFoundError:
        logging.error("Файл data/processed/matches.csv не найден")
        st.error("Данные не найдены. Запустите scripts/run_all.py")
        return None

df = load_data()
if df is None:
    st.stop()

# Навигация
st.sidebar.header("Навигация")
page = st.sidebar.radio("Выберите раздел", ["Главная", "Данные", "EDA", "Тренды", "Выводы"])

if page == "Главная":
    st.header("Добро пожаловать!")
    st.markdown("""
    Этот проект анализирует сезон ФК Барселона 2024/2025. Источник данных: веб-скрэпинг (fbref.com).
    - **Сбор данных**: Парсинг матчей и бомбардиров.
    - **Очистка**: Приведение к DataFrame, удаление пропусков.
    - **Анализ**: Тренды голов, сравнение дома/в гостях, результаты.
    - **Дэшборд**: Интерактивные фильтры и графики.
    Используйте меню слева для навигации.
    """)

elif page == "Данныеdff = load_data()
if df is None:
    st.stop()

# Фильтры
st.sidebar.header("Фильтры")
matchday_range = st.sidebar.slider("Выберите туры", int(df['matchday'].min()), int(df['matchday'].max()), (1, int(df['matchday'].max())))
venue_filter = st.sidebar.multiselect("Место проведения", options=df['venue'].unique(), default=df['venue'].unique())
result_filter = st.sidebar.multiselect("Результат", options=df['result'].unique(), default=df['result'].unique())
filtered_df = df[
    (df['matchday'].between(matchday_range[0], matchday_range[1])) &
    (df['venue'].isin(venue_filter)) &
    (df['result'].isin(result_filter))
]

st.header("Исходные данные")
st.dataframe(filtered_df, use_container_width=True)
st.write(f"Всего записей: {len(filtered_df)}")
st.write(f"Пропуски: {filtered_df.isnull().sum().sum()}")

elif page == "EDA":
    st.header("Разведывательный анализ данных (EDA)")
    st.subheader("Типы данных")
    st.write(df.dtypes)
    st.subheader("Описательные статистики")
    st.write(df.describe(include='all'))
    st.subheader("Пропуски")
    st.write(df.isnull().sum())
    st.subheader("Распределение результатов")
    fig = px.histogram(df, x='result', title='Распределение результатов матчей')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Тренды":
    st.header("Тренды и закономерности")
    st.subheader("Голы по турам")
    fig = px.line(filtered_df, x='matchday', y='goals_for', title='Голы Барселоны по турам', markers=True)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Голы: Дома vs В гостях")
    home_away = filtered_df.groupby('venue')['goals_for'].mean().reset_index()
    fig = px.bar(home_away, x='venue', y='goals_for', title='Средние голы по месту проведения', color='venue')
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Распределение результатов")
    fig = px.histogram(filtered_df, x='result', title='Распределение результатов матчей', color='result')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Выводы":
    st.header("Выводы и рекомендации")
    st.markdown("""
    ### Ключевые выводы
    - **Тренды голов**: Количество забитых голов варьируется, с пиками в домашних матчах.
    - **Дом/Гость**: Барселона забивает в среднем больше дома (на основе текущих данных).
    - **Результаты**: Команда показывает сбалансированное распределение побед, ничьих и поражений.
    - **Бомбардиры**: Данные о бомбардирах требуют доработки парсинга для точности.

    ### Рекомендации
    - Улучшить парсинг для получения данных о владении мячом и ударах.
    - Добавить анализ формы команды (например, процент побед за последние 5 матчей).
    - Интегрировать данные о травмах игроков для корреляции с результатами.

    ### Дальнейшие шаги
    - Автоматизировать обновление данных с помощью CI/CD на GitHub.
    - Добавить предсказание результатов матчей с использованием scikit-learn.
    """)
