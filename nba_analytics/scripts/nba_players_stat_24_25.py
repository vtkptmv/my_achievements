# nba_data_players_24_25.py

import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from tqdm import tqdm
import time
import os

# Створюємо папку для збереження даних, якщо не існує
os.makedirs("../data", exist_ok=True)

def get_active_players():
    """
    Отримує список лише активних гравців NBA.
    """
    all_players = players.get_active_players()
    return all_players

def get_player_game_stats(season="2024-25"):
    """
    Завантажує статистику по іграх усіх активних гравців за вказаний сезон.
    """
    active_players = get_active_players()
    all_data = []

    # tqdm - показує прогресбар по гравцях
    for player in tqdm(active_players, desc="Завантаження гравців"):
        player_id = player['id']
        player_name = player['full_name']

        try:
            # Отримуємо геймлог гравця за регулярний сезон
            gamelog = playergamelog.PlayerGameLog(
                player_id=player_id,
                season=season,
                season_type_all_star='Regular Season'
            )
            df = gamelog.get_data_frames()[0]
            df['PLAYER_NAME'] = player_name
            all_data.append(df)

            time.sleep(0.6)  # важливо: API обмежене, робимо паузу

        except Exception as e:
            print(f"⚠️ Помилка при обробці {player_name}: {e}")

    if all_data:
        full_df = pd.concat(all_data, ignore_index=True)
        full_df.to_csv("../data/nba_players_stat_24_25.csv", index=False)
        print("✅ Дані збережено у: data/nba_players_stat_24_25.csv")
    else:
        print("❌ Не вдалося зібрати жодної статистики.")

if __name__ == "__main__":
    get_player_game_stats()
