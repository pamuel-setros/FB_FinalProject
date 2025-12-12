import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('browns_data.db')
cursor = conn.cursor()

print("=" * 80)
print("CONSOLIDATING SQLITE DATABASE TO SINGLE TABLE")
print("=" * 80)

# Get the data from games table (the most comprehensive)
games_df = pd.read_sql_query("SELECT * FROM games", conn)

print(f"\nKeeping 'games' table with {len(games_df)} rows and {len(games_df.columns)} columns")

# Drop the other tables
cursor.execute("DROP TABLE IF EXISTS browns_stats")
cursor.execute("DROP TABLE IF EXISTS opponents_stats")
cursor.execute("DROP TABLE IF EXISTS browns_opp_data")

print("\nDropped tables:")
print("  - browns_stats")
print("  - opponents_stats")
print("  - browns_opp_data")

conn.commit()

# Verify only one table remains
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("\n" + "=" * 80)
print("REMAINING TABLES IN DATABASE:")
print("=" * 80)
for table in tables:
    print(f"  - {table[0]}")

# Display schema of the games table
print("\n" + "=" * 80)
print("GAMES TABLE SCHEMA:")
print("=" * 80)
cursor.execute("PRAGMA table_info(games)")
columns = cursor.fetchall()
for col in columns:
    print(f"  {col[1]}: {col[2]}")

print(f"\nTotal rows in 'games' table: {len(games_df)}")
print("\n" + "=" * 80)

conn.close()

print("Database consolidated to single 'games' table successfully!")
