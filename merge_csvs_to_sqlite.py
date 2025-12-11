import pandas as pd
import sqlite3

# Read both CSV files
browns_df = pd.read_csv('browns_12_percent_data.csv')
opponents_df = pd.read_csv('opponents_12_percent_data.csv')

# Merge the dataframes on Week and Opponent
# The opponents CSV uses 'Opponent_Team' to match 'Opponent' in browns CSV
merged_df = pd.merge(
    browns_df,
    opponents_df,
    left_on=['Week', 'Opponent'],
    right_on=['Week', 'Opponent_Team'],
    how='inner'
)

# Drop the redundant 'Opponent_Team' column
merged_df = merged_df.drop('Opponent_Team', axis=1)

# Create a connection to SQLite database
conn = sqlite3.connect('browns_data.db')

# Write the merged dataframe to the SQLite database
merged_df.to_sql('games', conn, if_exists='replace', index=False)

# Also create separate tables for reference
browns_df.to_sql('browns_stats', conn, if_exists='replace', index=False)
opponents_df.to_sql('opponents_stats', conn, if_exists='replace', index=False)

# Commit and close the connection
conn.commit()
conn.close()

print("Successfully merged CSV files into browns_data.db")
print(f"Merged table 'games' with {len(merged_df)} rows")
print(f"Browns stats table with {len(browns_df)} rows")
print(f"Opponents stats table with {len(opponents_df)} rows")
print("\nColumns in merged 'games' table:")
print(list(merged_df.columns))
