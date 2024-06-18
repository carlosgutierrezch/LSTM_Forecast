import pandas as pd
from datetime import datetime
class TimeConfig:


    def __init__(self):
        pass
    
    def time_transformation(df: pd.DataFrame,columns=list)-> pd.DataFrame:
        
        """_summary_
        
        Args:
            df (pd.DataFrame): Time Series DataFrame

        Returns:
            _type_: Time Series DataFrame
        """
        
        if 'Date' not in columns:                                                        # To add the 'Date' column to df
            columns.append('Date')

        df= df[columns].copy()                                   
                              
        for column in columns:
            if column != 'Date' and df[column].dtype == 'object':
                df[column]= df[column].str.replace('$','',regex=False).astype(float)     # Replacing the $ value
                        
        df['Date']= pd.to_datetime(df['Date'])                                           # To datetime
        
        df.sort_values(by='Date',inplace=True)                                              
        
        df.reset_index(inplace=True)
        
        df.drop(columns='index',inplace=True)
        
        df.set_index('Date',inplace=True)
        
        df.rename(columns={"Close/Last":"Value"},inplace=True)
        
        return df
    
    def time_features(df: pd.DataFrame)-> pd.DataFrame:
        
        """Function that receives time series data
        and retrieves a transformed dataframe with
        time features

        Args:
            df (pd.DataFrame): Time Series DataFrame

        Returns:
            pd.DataFrame: Time Series DataFrame with
            features
        """
        
        df['week']= df.index.dayofweek              # DatetimeIndex functions for feature engineering
        df['month']= df.index.month
        df['year']= df.index.year
        df['day_of_week']= df.index.day_name()
        df['quarter']= df.index.quarter
        
        return df
    
    def time_change(df: pd.DataFrame)-> pd.DataFrame:
    
        """Function that evaluate the increase or decrease of the Value
        over the years of all the dataset
        
        Args:
            df (pd.DataFrame): Time Series DataFrame
        
        Returns:
            _type_: Groupby Dataset with all the transformations
        """
        
        df= df.groupby(df.index.year).agg({'Value':'sum'}).astype(int)         # Gathering of data
        nuevo= df.iloc[:,0].tolist()                                                 
        
        empty_list= []
        for i in range(1,len(nuevo)):
            difference= (nuevo[i]-nuevo[i-1])/nuevo[i-1]*100                        # Calculating the change
            empty_list.append(difference)
            
        if len(nuevo) != len(empty_list):                                           # Adding the information the the dataset
            df["change"]= [0]+empty_list
            df.change= df.change.astype(int)
        
            
        return df
    

   