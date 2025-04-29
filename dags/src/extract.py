# extract.py

import pyodbc
import pandas as pd
import json

# Load SQL Server config
with open('config_pipeline/sqlserver_config.json') as f:
    sql_config = json.load(f)

def get_sqlserver_connection():
    connection = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={sql_config['server']};"
        f"DATABASE={sql_config['database']};"
        f"UID={sql_config['username']};"
        f"PWD={sql_config['password']}"
    )
    return connection

def extract_table(table_name):
    conn = get_sqlserver_connection()
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    conn.close()
    print(f"✅ Extracted {len(df)} records from {table_name}")
    return df

if __name__ == "__main__":
    # Extract all three tables
    players_df = extract_table('players')
    matches_df = extract_table('matches')
    player_stats_df = extract_table('player_stats')

    # Optional: Save to CSV temporarily (for debug)
    players_df.to_csv('players_data.csv', index=False)
    matches_df.to_csv('matches_data.csv', index=False)
    player_stats_df.to_csv('player_stats_data.csv', index=False)
