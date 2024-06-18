import pandas as pd
from datetime import datetime
class AppleFeature:


    def __init__(self):
        pass
    
    def time_features(self,df: pd.DataFrame)-> pd.DataFrame:
        
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
    
    def time_change(df:pd.DataFrame)-> pd.DataFrame:
    
        """Function that evaluate the increase or decrease of the Value
        over the years of all the dataset
        
        Returns:
            _type_: Groupby Dataset with all the transformations
        """
        
        df= df.groupby(df.index.year).agg({'Close/Last':'sum'}).astype(int)         # Gathering of data
        df.rename(columns={'Close/Last':'Value'},inplace=True)                      # Renaming
        nuevo= df.iloc[:,0].tolist()                                                 
        
        empty_list= []
        for i in range(1,len(nuevo)):
            difference= (nuevo[i]-nuevo[i-1])/nuevo[i-1]*100                        # Calculating the change
            empty_list.append(difference)
            
        if len(nuevo) != len(empty_list):                                           # Adding the information the the dataset
            df["change"]= [0]+empty_list
            df.change= df.change.astype(int)
            
            
        return df  