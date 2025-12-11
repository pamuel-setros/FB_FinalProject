import csv
from bs4 import BeautifulSoup
import os

# --- CONFIGURATION ---
INPUT_FILE = 'browns_pfr.html'
OUTPUT_FILE = 'browns_12_percent_data.csv'

# Calculated from your screenshot: 49 Team Drops / 17 Games
AVG_DROPS_PER_GAME = 2.88

def scrape_12_percent_data():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: '{INPUT_FILE}' not found.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Locate the Regular Season table
    table = soup.find('table', id="table_pfr_team-year_game-logs_team-year-regular-season-game-log")
    
    if not table:
        print("Could not find the game log table. Check the HTML file.")
        return

    # Prepare CSV Output
    headers = [
        'Week', 'Opponent', 'Result', 
        'Total_Plays', 'Sacks', 'Turnovers', 'Penalties', 'Est_Drops',
        'Total_Critical_Errors', '12_Percent_Score', 'Win_Loss_Bool'
    ]
    
    rows_data = []

    # Parse rows (skip thead)
    tbody = table.find('tbody')
    for tr in tbody.find_all('tr'):
        # Skip sub-headers or breaks
        if 'thead' in tr.get('class', []):
            continue

        # Helper function to get int values safely
        def get_val(stat_name):
            cell = tr.find('td', {'data-stat': stat_name})
            text = cell.get_text(strip=True) if cell else '0'
            return int(text) if text.isdigit() else 0

        # Extract Basic Info
        week = tr.find('td', {'data-stat': 'week_num'}).get_text(strip=True)
        opp = tr.find('td', {'data-stat': 'opp_name_abbr'}).get_text(strip=True)
        result_text = tr.find('td', {'data-stat': 'team_game_result'}).get_text(strip=True)
        
        # Determine Win/Loss (1 for Win, 0 for Loss) for your analytics later
        is_win = 1 if result_text.upper().startswith('W') else 0

        # Extract "12% Rule" Components
        plays = get_val('plays_offense')
        sacks = get_val('pass_sacked')
        turnovers = get_val('turnovers')
        penalties = get_val('penalties') # Using total penalties as proxy for "bad penalties"
        
        # Calculate Logic
        # If plays is 0 (e.g. game hasn't happened), skip to avoid division by zero
        if plays > 0:
            total_errors = sacks + turnovers + penalties + AVG_DROPS_PER_GAME
            score_percentage = (total_errors / plays) * 100
            
            rows_data.append([
                week,
                opp,
                result_text,
                plays,
                sacks,
                turnovers,
                penalties,
                AVG_DROPS_PER_GAME,
                round(total_errors, 2),
                round(score_percentage, 2), # This is your "12% Score"
                is_win
            ])

    # Write to CSV
    try:
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows_data)
        print(f"Success! Processed {len(rows_data)} games into '{OUTPUT_FILE}'.")
        print(f"Average Drops ({AVG_DROPS_PER_GAME}) added to every week.")
    except Exception as e:
        print(f"Error writing CSV: {e}")

if __name__ == "__main__":
    scrape_12_percent_data()