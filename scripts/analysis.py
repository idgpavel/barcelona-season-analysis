import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def plot_goals(df, save_path='visualizations/goals_per_matchday.png'):
    try:
        os.makedirs('visualizations', exist_ok=True)
        required_columns = ['matchday', 'goals_for']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Отсутствуют столбцы: matchday, goals_for")
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df, x='matchday', y='goals_for', marker='o', label='Голы за')
        plt.title('Голы Барселоны по турам', fontsize=14)
        plt.xlabel('Тур', fontsize=12)
        plt.ylabel('Голы', fontsize=12)
        plt.grid(True)
        plt.legend()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        logging.info(f"График сохранён в {save_path}")
    except Exception as e:
        logging.error(f"Ошибка при создании графика: {e}")

def plot_home_away_goals(df, save_path='visualizations/home_away_goals.png'):
    try:
        home_away = df.groupby('venue')['goals_for'].mean().reset_index()
        plt.figure(figsize=(8, 5))
        sns.barplot(data=home_away, x='venue', y='goals_for', palette='viridis')
        plt.title('Средние голы: Дома vs В гостях', fontsize=14)
        plt.xlabel('Место', fontsize=12)
        plt.ylabel('Средние голы', fontsize=12)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        logging.info(f"График сохранён в {save_path}")
    except Exception as e:
        logging.error(f"Ошибка при создании графика: {e}")

def plot_results_distribution(df, save_path='visualizations/results_distribution.png'):
    try:
        plt.figure(figsize=(8, 5))
        sns.countplot(data=df, x='result', palette='muted', order=['W', 'D', 'L'])
        plt.title('Распределение результатов матчей', fontsize=14)
        plt.xlabel('Результат (W: Победа, D: Ничья, L: Поражение)', fontsize=12)
        plt.ylabel('Количество матчей', fontsize=12)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        logging.info(f"График сохранён в {save_path}")
    except Exception as e:
        logging.error(f"Ошибка при создании графика: {e}")

if __name__ == "__main__":
    try:
        df = pd.read_csv('data/processed/matches.csv')
        plot_goals(df)
        plot_home_away_goals(df)
        plot_results_distribution(df)
    except FileNotFoundError:
        logging.error("Файл data/processed/matches.csv не найден")
