import pandas as pd
import sqlite3

# Read the CSV file into a pandas dataframe
df = pd.read_csv('browns_opp_data.csv')

print("=" * 80)
print("BROWNS OPPONENTS DATA - PANDAS DATAFRAME")
print("=" * 80)
print(f"\nDataframe Shape: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"\nData Types:\n{df.dtypes}")
print(f"\nFirst few rows:\n{df.head()}")

# Insert into SQLite database
print("\n" + "=" * 80)
print("INSERTING INTO SQLITE DATABASE")
print("=" * 80)

conn = sqlite3.connect('browns_data.db')

# Insert as a new table
df.to_sql('browns_opp_data', conn, if_exists='replace', index=False)

print(f"\nSuccessfully inserted {len(df)} rows into 'browns_opp_data' table")

# Verify the data
result = pd.read_sql_query("SELECT * FROM browns_opp_data LIMIT 5", conn)
print(f"\nVerification - Sample data from database:\n{result}")

conn.close()

print("\n" + "=" * 80)
print("Dataframe is now available in SQLite as 'browns_opp_data' table")
print("=" * 80)
