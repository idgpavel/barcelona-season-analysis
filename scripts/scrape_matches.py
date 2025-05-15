import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import os
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_matches(url='https://fbref.com/en/squads/206d90db/Barcelona-Stats'):
    try:
        os.makedirs('data/raw', exist_ok=True)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        # response = requests.get(url, headers=headers)
        # response.raise_for_status()
        # soup = BeautifulSoup(response.text, 'html.parser')
        
        # Заглушка: генерация 100 матчей
        start_date = datetime(2024, 8, 15)
        opponents = ['Real Madrid', 'Atletico', 'Sevilla', 'Betis', 'Valencia']
        venues = ['Home', 'Away']
        scorers = ['Lewandowski', 'Raphinha', 'Yamal', None]
        data = []
        for i in range(100):
            date = start_date + timedelta(days=i*7)
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'opponent': opponents[i % len(opponents)],
                'goals_for': (i % 4) + 1,
                'goals_against': (i % 3),
                'venue': venues[i % 2],
                'top_scorer': scorers[i % len(scorers)],
                'result': ['W', 'D', 'L'][i % 3]
            })
        df = pd.DataFrame(data)
        df.to_csv('data/raw/matches.csv', index=False)
        logging.info("Данные матчей сохранены в data/raw/matches.csv")
        return df
    except Exception as e:
        logging.error(f"Ошибка при парсинге: {e}")
        return None

if __name__ == "__main__":
    scrape_matches()
