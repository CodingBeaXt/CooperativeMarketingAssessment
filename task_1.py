# Task 1
"""Module demonstrating data manipulation basics with pandas and numpy."""

import numpy as np
import pandas as pd


def create_dataframe():
    """Creates a DataFrame with initial data."""
    data = {
        'score_1': [0.1, 0.05, 0.3, 0.15],
        'score_2': [0.2, 0.8, 0.6, 0.1]
    }
    return pd.DataFrame(data)

def add_highlighted_column(df):
    """Adds a 'highlighted' column to the DataFrame based on specific logic."""
    df['highlighted'] = (
        ((df['score_1'] < 0.35) & (df['score_2'] < 0.35)) |
        ((df['score_1'] < 0.20) & (df['score_2'] < 0.90)) |
        ((df['score_1'] < 0.15) & (df['score_2'] < 0.80))
    )

def add_risk_1_group_column(df):
    """Adds a 'risk_1_group' categorical column to the DataFrame based on 'score_1' values."""
    conditions = [
        (df['score_1'] < 0.10),
        (df['score_1'] >= 0.10) & (df['score_1'] < 0.30),
        (df['score_1'] >= 0.30) & (df['score_1'] < 0.80),
        (df['score_1'] >= 0.80)
    ]
    choices = ['Very Low', 'Medium', 'High', 'Very High']
    df['risk_1_group'] = pd.Categorical(
        np.select(conditions, choices, default='Unknown'),
        categories=choices + ['Unknown'],
        ordered=True
    )

def main():
    """Main function to demonstrate data manipulation."""
    df = create_dataframe()
    add_highlighted_column(df)
    add_risk_1_group_column(df)
    print(df)

if __name__ == "__main__":
    main()
