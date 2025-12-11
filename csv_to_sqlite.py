import pandas as pd
import sqlite3

# Read the CSV file
df = pd.read_csv('browns_12_percent_data.csv')

# Create a connection to SQLite database
conn = sqlite3.connect('browns_12_percent_data.db')

# Write the dataframe to the SQLite database
df.to_sql('browns_data', conn, if_exists='replace', index=False)

# Commit and close the connection
conn.commit()
conn.close()

print("Successfully converted browns_12_percent_data.csv to browns_12_percent_data.db")
print(f"Total rows inserted: {len(df)}")
