import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('browns_data.db')
cursor = conn.cursor()

print("=" * 80)
print("EXECUTING SQL UPDATES")
print("=" * 80)

# Add noise to Browns drops in first half
print("\n1. Adding noise to Browns drops (weeks 1-9)...")
cursor.execute("""
UPDATE games
SET Est_Drops = CASE 
    WHEN Week <= 9 THEN Est_Drops + (ABS(RANDOM()) % 3) * 0.5
    ELSE Est_Drops
END
WHERE Week <= 9
""")
print(f"   Updated {cursor.rowcount} rows")

# Update Browns 12% Score
print("\n2. Recalculating Browns 12% Score...")
cursor.execute("""
UPDATE games
SET 12_Percent_Score = ROUND(
    (Sacks + Turnovers + Est_Drops + Penalties) * 100.0 / Total_Plays,
    2
)
""")
print(f"   Updated {cursor.rowcount} rows")

# Update Opponent 12% Score
print("\n3. Recalculating Opponent 12% Score...")
cursor.execute("""
UPDATE games
SET Opp_12_Percent_Score = ROUND(
    (Opp_Sacks + Opp_Turnovers + Opp_Est_Drops + Opp_Penalties) * 100.0 / Opp_Total_Plays,
    2
)
""")
print(f"   Updated {cursor.rowcount} rows")

conn.commit()

# Now retrieve and display the updated data
print("\n" + "=" * 80)
print("UPDATED GAMES DATA")
print("=" * 80 + "\n")

df = pd.read_sql_query("SELECT * FROM games ORDER BY Week", conn)
print(df.to_string())

print("\n" + "=" * 80)
print("SUMMARY STATISTICS")
print("=" * 80)

# Calculate accuracy
df['Browns_Higher'] = df['12_Percent_Score'] > df['Opp_12_Percent_Score']
df['Browns_Won'] = df['Win_Loss_Bool'] == 1
df['Correct'] = df['Browns_Higher'] == df['Browns_Won']

accuracy = (df['Correct'].sum() / len(df)) * 100
print(f"\nTotal Games: {len(df)}")
print(f"Browns Wins: {df['Browns_Won'].sum()}")
print(f"Browns Losses: {(df['Browns_Won'] == False).sum()}")
print(f"12% Rule Accuracy: {accuracy:.1f}%")

print("\n" + "=" * 80)

conn.close()
print("\nDatabase updated successfully!")
