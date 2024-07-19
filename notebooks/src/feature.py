"""
This module contains the TimeConfig class, which provides methods for transforming time series
data and adding time-based features.
"""
import os
import logging
import pandas as pd
from pathlib import Path
logging.basicConfig(level=logging.INFO,format='%(asctime)s,%(levelname)s,%(message)s')
class TimeConfig:
    """
    A class used to represent time configuration for various operations on time series data.
    """
    @staticmethod
    def data_ingestion(path: str )->pd.DataFrame:
        """
        Ingest data from a path and retrieves a Pandas DataFrame

        Args:
            path (str): String path to the document

        Returns:
            pd.DataFrame: Pandas Dataframe object
        """
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"File not found: {path}")
            _,file_extension= os.path.splitext(path)

            if file_extension == '.csv':
                df = pd.read_csv(path,sep=',',encoding='utf-8')
            elif file_extension in ['.xlsx','.xls']:
                df = pd.read_excel(path)
            elif file_extension == '.json':
                df = pd.read_json(path)
            else:
                raise ValueError(f"Unsupported File Extension{file_extension}")
            return df

        except FileNotFoundError:
            print(f"File not found:{path}")
        except pd.errors.EmptyDataError:
            print(f"No data: The file at the path {path} is empty")
        except pd.errors.ParserError:
            print(f"Parsing error: The data at {path} could not be parsed")
        except IOError as e:
            print(f"IO eror: {e}")
        except ValueError as e:
            print(f"Value error: {e}")
        return pd.DataFrame()

    @staticmethod
    def time_transformation(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """
        Transforms the time series DataFrame to include specified columns.

        Args:
            df (pd.DataFrame): Time Series DataFrame
            columns (list): List of column names to retain in the transformed DataFrame

        Returns:
            pd.DataFrame: Transformed Time Series DataFrame
        """
        if 'Date' not in columns:
            columns.append('Date')

        missing_columns= [col for col in columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing columns in the dataframe: {missing_columns}")

        df = df[columns].copy()

        df['Date'] = pd.to_datetime(df['Date'])

        df.sort_values(by='Date', inplace=True)

        df.reset_index(inplace=True, drop=True)

        df.set_index('Date', inplace=True)

        for column in columns:
            if column != 'Date' and df[column].dtype == 'object':
                df[column] = df[column].str.replace('$', '', regex=False).astype(float)
        if 'Close/Last' in columns:
            df.rename(columns={'Close/Last':'Value'},inplace=True)

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
        if 'Value' not in df.columns:
            raise ValueError("Column 'Value' not found in DataFrame")
        x_1= df.groupby(df.index.year).agg({'Value':'sum'}).astype(int).copy()
        x_2= x_1.Value.tolist()
        diferencias = []
        for i in range(1, len(x_2)):
            diferencia = int((x_2[i] - x_2[i-1]) / x_2[i-1] * 100)
            diferencias.append(diferencia)

        x_1['Change']= [0]+diferencias

        return x_1

    @staticmethod
    def process_chain(path:str,columns=list[str])-> pd.DataFrame:
        """
        Pipeline of data transformatiuon

        Args:
            path (str): path to data
            columns (_type_, optional): Columns to transform

        Returns:
            pd.DataFrame: DataFrame transformed
        """
        df= TimeConfig.data_ingestion(path)
        if not df.empty:
            df= TimeConfig.time_transformation(df,columns)
        return df
