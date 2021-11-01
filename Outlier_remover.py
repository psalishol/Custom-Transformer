import pandas as pd
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
class OutlierRemover(TransformerMixin, BaseEstimator):
    
    def __init__(self,
                 dependent_col=None,
                 estimator= None,
                 regression=False
                 ):
        self.estimator = estimator
        self.dependent = dependent_col
        self.reg = regression
        
        if estimator is None:
            raise ValueError(
                """ Input an estimator """
                """ The estimator can be KNeigbourRegressor or RandomForestRegressor"""
                )
    
    def fit(self, X, Y):
        if self.reg is False:
            chk_fea = [
                        feature for feature in X.columns
                            if X[feature].dtype != object and X[feature].nunique() > 7
                    ]
            for feature in X[chk_fea].columns:
                
                Q1 = X[feature].quantile(0.25)   ###Lowe quantile
                Q3 = X[feature].quantile(0.75)   ###Upper quantile
                IQR = Q3 - Q1    ###Interquantile range
                lower_boundary = Q1 - (1.5 * IQR)
                upper_boundary = Q3 + (1.5 * IQR)

                ###Replacing the outlier with a nan value
                X.loc[X[feature] > upper_boundary, feature] = np.nan
                X.loc[X[feature] < lower_boundary, feature] = np.nan
            return self
        if self.reg is True:
            new_data = pd.concat([X,Y],axis="columns")
            chk_fea = [
                        feature for feature in new_data.columns
                            if new_data[feature].dtype != object and new_data[feature].nunique() > 7
                    ]
            for feature in X[chk_fea].columns:
                
                Q1 = new_data[feature].quantile(0.25)   ###Lowe quantile
                Q3 = new_data[feature].quantile(0.75)   ###Upper quantile
                IQR = Q3 - Q1    ###Interquantile range
                lower_boundary = Q1 - (1.5 * IQR)
                upper_boundary = Q3 + (1.5 * IQR)

                ###Replacing the outlier with a nan value
                new_data.loc[X[feature] > upper_boundary, feature] = np.nan
                new_data.loc[X[feature] < lower_boundary, feature] = np.nan
            return self
        
    def transform(self, X, Y):
        if self.reg is False:
            data_copy = X.copy()
            chk_fea = [
                feature for feature in X.columns 
                        if X[feature].dtype != object and X[feature].nunique() > 7
            ]
            d_chk = [
                feature for feature in X.columns
                    if X[feature].dtype != object and X[feature].nunique() <= 7
            ]
            cat_feature = [
                feature for feature in X.columns
                        if X[feature].dtype == object
            ]
            transformer = IterativeImputer(
                        estimator = self.estimator, random_state=42, max_iter=5,verbose=0
            )
            transformer.fit(X[chk_fea])
            transformed = transformer.transform(X[chk_fea])
            transformed_data = pd.DataFrame(transformed,columns=X[chk_fea].columns)
            X = pd.concat([transformed_data,X[d_chk],X[cat_feature]], axis=1)
            return X
        if self.reg is True:
            new_data = pd.concat([X,Y],axis=1)
            chk_fea = [
                feature for feature in new_data.columns 
                        if new_data[feature].dtype != object and new_data[feature].nunique() > 7
            ]
            d_chk = [
                feature for feature in new_data.columns
                    if new_data[feature].dtype != object and new_data[feature].nunique() <= 7
            ]
            cat_feature = [
                feature for feature in new_data.columns
                        if new_data[feature].dtype == object
            ]
            transformer = IterativeImputer(
                        estimator = self.estimator, random_state=42, max_iter=5,verbose=0
            )
            transformer.fit(new_data[chk_fea])
            transformed = transformer.transform(new_data[chk_fea])
            transformed_data = pd.DataFrame(transformed,columns=new_data[chk_fea].columns)
            transformed_data_X = transformed_data.drop(self.dependent, axis="columns")
            X = pd.concat([tranformed_data_X,X[d_chk],X[cat_feature]], axis="columns")
            
            return X
            
