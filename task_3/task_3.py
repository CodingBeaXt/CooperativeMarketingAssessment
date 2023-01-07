# TASK 3
"""Module description: This module contains code for reading and manipulating a CSV file."""

import os

import pandas as pd

current_directory = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(current_directory, 'task3_dateset.csv')

try:
    df = pd.read_csv(csv_file_path)
    print("CSV file loaded successfully!")
except FileNotFoundError:
    print(f"Error: File '{csv_file_path}' not found.")

print('Reading the file:')
print(df)

df = df[::-1].reset_index(drop=True)

df['Corrected_Ads_Run'] = df['Ads_Run']

for i in range(len(df) - 1, -1, -1):
    if df.at[i, 'Ads_Run'] == 0:
        df.at[i, 'Corrected_Ads_Run'] = df.at[i + 1, 'Ads_Run'] if i + 1 < len(df) else 0

df = df[::-1].reset_index(drop=True)

print('Adding Corrected_Ads_Run column:')
print(df)
