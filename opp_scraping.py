import csv
from bs4 import BeautifulSoup
import os

# --- CONFIGURATION ---
INPUT_FILE = 'browns_pfr.html'
OUTPUT_FILE = 'opponents_12_percent_data.csv'

# Standard estimate for opponents (Since they didn't have Amari Cooper)
OPPONENT_DROPS = 3.0 

def scrape_opponent_stats():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: '{INPUT_FILE}' not found.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # 1. Target the Opponent Game Log Table
    # Note the ID change: "...-opponent-game-log"
    table_id = "table_pfr_team-year_game-logs_team-year-regular-season-opponent-game-log"
    table = soup.find('table', id=table_id)
    
    if not table:
        print(f"Error: Could not find table with ID: {table_id}")
        return

    headers = [
        'Week', 'Opponent_Team', 'Cleveland_Result', 
        'Opp_Total_Plays', 'Opp_Sacks', 'Opp_Turnovers', 'Opp_Penalties', 'Opp_Est_Drops',
        'Opp_Total_Errors', 'Opp_12_Percent_Score', 'Opp_Is_Win'
    ]
    
    csv_rows = []
    tbody = table.find('tbody')

    for tr in tbody.find_all('tr'):
        if 'thead' in tr.get('class', []):
            continue

        # Helper to safely get data
        def get_int(stat_name):
            cell = tr.find('td', {'data-stat': stat_name})
            val = cell.get_text(strip=True) if cell else '0'
            return int(val) if val.isdigit() else 0

        # Basic Info
        week = tr.find('td', {'data-stat': 'week_num'}).get_text(strip=True)
        opp_name = tr.find('td', {'data-stat': 'opp_name_abbr'}).get_text(strip=True)
        cle_result = tr.find('td', {'data-stat': 'team_game_result'}).get_text(strip=True)

        # Logic: If Cleveland Won (W), the Opponent Lost (0). If Cleveland Lost (L), Opponent Won (1).
        opp_is_win = 0 if cle_result.upper().startswith('W') else 1

        # Opponent Stats (In this specific table, 'plays_offense' refers to the Opponent's plays)
        plays = get_int('plays_offense')
        sacks = get_int('pass_sacked')
        turnovers = get_int('turnovers')
        penalties = get_int('penalties')
        
        # Calculate Score
        if plays > 0:
            total_errors = sacks + turnovers + penalties + OPPONENT_DROPS
            score_pct = (total_errors / plays) * 100
            
            csv_rows.append([
                week,
                opp_name,
                cle_result,
                plays,
                sacks,
                turnovers,
                penalties,
                OPPONENT_DROPS,
                total_errors,
                round(score_pct, 2),
                opp_is_win
            ])

    # Write to CSV
    try:
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(csv_rows)
        print(f"Success! Scraped opponent data for {len(csv_rows)} games.")
        print(f"Saved to: {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error writing CSV: {e}")

if __name__ == "__main__":
    scrape_opponent_stats()