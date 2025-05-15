import logging
from scrape_matches import scrape_matches
from data_cleaning import clean_data, perform_eda
from analysis import plot_goals, plot_home_away_goals, plot_results_distribution

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Запуск полного цикла анализа...")
    df = scrape_matches()
    if df is None:
        logging.error("Не удалось собрать данные")
        return
    df_cleaned = clean_data(df)
    if df_cleaned is None:
        logging.error("Не удалось очистить данные")
        return
    perform_eda(df_cleaned)
    plot_goals(df_cleaned)
    plot_home_away_goals(df_cleaned)
    plot_results_distribution(df_cleaned)
    logging.info("Анализ завершён. Запустите 'streamlit run dashboard/app.py' для просмотра дэшборда.")

if __name__ == "__main__":
    main()
