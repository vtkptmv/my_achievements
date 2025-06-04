from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd
import os

print("Завантаження ігор сезону 2024-25...")

# 1. Отримуємо всі ігри (регулярний сезон + плейофф) для сезону 2024-25
games = leaguegamefinder.LeagueGameFinder(season_nullable='2024-25')  # Може не працювати, якщо сезон ще не почався
all_games = games.get_data_frames()[0]

# 2. Перевірка: чи є дані та чи містять колонку 'LEAGUE_ID'
if not all_games.empty and 'LEAGUE_ID' in all_games.columns:
    
    # 3. Фільтруємо лише ігри регулярного сезону NBA
    nba_regular = all_games[
        (all_games['SEASON_ID'].str.endswith('24')) &  # '24' в кінці = регулярка 2024-25
        (all_games['LEAGUE_ID'] == '00')               # '00' = NBA, а не G-League
    ]

    # 4. Створюємо директорію, якщо не існує
    os.makedirs("../data", exist_ok=True)

    # 5. Зберігаємо дані у CSV
