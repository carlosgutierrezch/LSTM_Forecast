"""
Series of classes for data transformation in LSTM-TORCH module
"""
import pandas as pd
import numpy as np

class  TransformLag:
    """
    Series of transformation from DataFrame tu numpy with all their variances

    Returns:
        _type_: Different set of values from pandas tu numpy
    """
    @staticmethod
    def transform_df(df:pd.DataFrame,n_steps:int)->pd.DataFrame:
        """
        Create lags from the 'Value' column to pass in a regressive way to the model

        Args:
            df (pd.DataFrame): Pandas DataFrame
            n_steps (int): Number of lags to create

        Returns:
            _type_: Pandas DataFrame with lags
        """

        for i in range(1,n_steps+1):
            df[f'Value (t-{i})']= df.iloc[:,0].shift(i)

        df.dropna(inplace=True)
        return df

    @staticmethod
    def lag_numpy(df:pd.DataFrame)-> np.ndarray:
        """
        Takes a Pandas DataFrame and make transformations to 
        return a numpy array of numbers

        Args:
            df (pd.DataFrame): Pandas DataFrame

        Returns:
            np.ndarray: Matrix with array of numbers
        """
        df=df.asfreq('D')
        df.ffill(inplace=True)
        data_array= df.to_numpy()
        return data_array

  
    @staticmethod
    def lag_transform(df:pd.DataFrame,n_steps:int)->pd.DataFrame:

        for i in range(1,n_steps+1):
            df[f'Value (t-{i})']= df.iloc[:,0].shift(i)

        df.dropna(inplace=True)
        df=df.asfreq('D')
        df.ffill(inplace=True)
        # data_array= df.to_numpy()
        return df
