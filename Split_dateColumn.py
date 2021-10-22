import pandas as pd
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.model_selection import train_test_split

class CreateTime(BaseEstimator,TransformerMixin):
    """
    Class for splitting Date column in a pandas dataframe to Year, Month and Day of week

    Parameters
    ----------
    dateColumn: Takes in the Date column to be splitted, Must be in  ```str``` format

    Year: boolean ```True``` / ```False```
            if True, Year variable would be added to the dataframe

    *Month*: boolean ```True``` / ```False```
            if True, Month variable would be added to the dataframe

    DayofWeek_int: boolean ```True``` / ```False```
    if True, Day of week variable with instance ranging from ```0``` to ```6``` would be added to the dataframe

    DayofWeek_obj: boolean ```True``` / ```False```: if True, Weekdays variable starting from Sunday to Saturday would be addedd to the dataframe
    """
    def __init__(self,dateColumn, 
                Year=True, Month=True, 
                DayofWeek_int=True, drop_column=True,
                DayofWeek_obj = False
                ):
        ###initializing all the set variables
        self.dateCol = dateColumn
        self.year = Year
        self.month = Month
        self.dayofweek_int = DayofWeek_int
        self.dayofweek_obj = DayofWeek_obj
        self.drop_column = drop_column
    
    ###Converts the Date to a readable pandas datetime
    def fit(self, X, y=None):
        ###fitting the dataset;
        X.loc[:,self.dateCol] = pd.to_datetime(X.loc[:,self.dateCol])
        return X    ##returns X with converted datetime.

    ###splits the data into Year, Month, Day of week, and Week day, base on input 
    def transform(self,X,y=None):

        if self.year:
            X.loc[:,"Year"] = X.loc[:,self.dateCol].apply(lambda date: date.year)
        else:
            return X
        if self.month:
            X.loc[:,"Month"] = X.loc[:,self.dateCol].apply(lambda date: date.month)
        else:
            return X
        if self.dayofweek_int:
            X.loc[:,"Day of week"] = X.loc[:,self.dateCol].apply(lambda date: date.dayofweek)
        else:
            return X
        if self.dayofweek_obj is True:
        ###Create a dict containing the weekdays
            day={
                0 : "Sun",
                1 : "Mon",
                2 : "Tues",
                3 : "Weds",
                4 : "Thurs",
                5 : "Fri",
                6 : "Sat"
            }
            X.loc[:,"Week"] = X.loc[:,self.dateCol].apply(lambda date: date.dayofweek)
            X.loc[:,"Week"] = X.loc[:,"Week"].map(day)
        else:
            return X
        if self.drop_column is False:
            return X
        else:
            X = X.drop(self.dateCol, axis="columns")
        return X
