"""
This module contains the TimeConfig class, which provides methods for transforming time series
data and adding time-based features.
"""

import pandas as pd

class TimeConfig:
    """
    A class used to represent time configuration for various operations on time series data.
    """

    @staticmethod
    def time_transformation(df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """
        Transforms the time series DataFrame to include specified columns.

        Args:
            df (pd.DataFrame): Time Series DataFrame
            columns (list): List of column names to retain in the transformed DataFrame

        Returns:
            pd.DataFrame: Transformed Time Series DataFrame
        """
        # Ensure 'Date' column is included
        if 'Date' not in columns:
            columns.append('Date')

        # Only taking specified columns
        df = df[columns].copy()

        # Process 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        # Sort by 'Date'
        df.sort_values(by='Date', inplace=True)

        # Reset index
        df.reset_index(inplace=True, drop=True)

        # Set 'Date' as the index
        df.set_index('Date', inplace=True)

        # Clean column names (removing '$' and converting to float if necessary)
        for column in columns:
            if column != 'Date' and df[column].dtype == 'object':
                df[column] = df[column].str.replace('$', '', regex=False).astype(float)

        return df

    @staticmethod
    def time_features(df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds time-based features to the DataFrame.

        Args:
            df (pd.DataFrame): Input DataFrame

        Returns:
            pd.DataFrame: DataFrame with time-based features
        """
        df['year'] = df.index.year
        df['month'] = df.index.month
        df['day'] = df.index.day
        df['day_of_week'] = df.index.dayofweek
        df['day_of_year'] = df.index.dayofyear
        df['week_of_year'] = df.index.isocalendar().week

        return df

    @staticmethod
    def time_change(df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds features representing changes in the DataFrame.

        Args:
            df (pd.DataFrame): Input DataFrame

        Returns:
            pd.DataFrame: DataFrame with change features
        """
        df['value_change'] = df['Value'].diff()
        df['value_pct_change'] = df['Value'].pct_change()

        return df
