import pandas as pd
import pytest
from scripts.data_cleaning import clean_data

def test_clean_data():
    df = pd.DataFrame({
        'Date': ['2024-08-15', '2024-08-15', None],
        'Opponent': ['Real Madrid', 'Real Madrid', 'Sevilla'],
        'Goals For': ['2', '2', '3'],
        'Goals Against': ['1', '1', '2'],
        'Venue': ['Home', 'Home', 'Away'],
        'Result': ['W', 'W', 'L']
    })
    df_cleaned = clean_data(df, output_path='data/processed/test_matches.csv')
    
    assert len(df_cleaned) == 2  # Дубликаты удалены
    assert all(col in ['date', 'opponent', 'goals_for', 'goals_against', 'venue', 'result', 'matchday'] for col in df_cleaned.columns)
    assert df_cleaned['goals_for'].dtype == 'int32'
    assert df_cleaned['date'].dtype == 'datetime64[ns]'

if __name__ == "__main__":
    pytest.main(["-v"])
