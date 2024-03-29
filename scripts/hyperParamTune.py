# Hyperparameter tuning : https://github.com/davidsbatista/machine-learning-notebooks/blob/master/hyperparameter-across-models.ipynb

import numpy as np
import pandas as pd

from sklearn.model_selection import GridSearchCV

class EstimatorSelectionHelper:
    
    def __init__(self, models, params):
        self.models = models
        self.params = params
        self.keys = models.keys()
        self.grid_searches = {}
    
    def fit(self, X, y, **grid_kwargs):
        for key in self.keys:
            print('Running GridSearchCV for %s.' % key)
            model = self.models[key]
            params = self.params[key]
            grid_search = GridSearchCV(model, params, **grid_kwargs)
            grid_search.fit(X, y)
            self.grid_searches[key] = grid_search
        print('Done.')
    
    def score_summary(self, sort_by='mean_test_score'):
        frames = []
        for name, grid_search in self.grid_searches.items():
            frame = pd.DataFrame(grid_search.cv_results_)
            frame = frame.filter(regex='^(?!.*param_).*$')
            frame['estimator'] = len(frame)*[name]
            frames.append(frame)
        df = pd.concat(frames)
        
        df = df.sort_values([sort_by], ascending=False)
        df = df.reset_index()
        df = df.drop(['rank_test_score', 'index'], 1)
        
        columns = df.columns.tolist()
        columns.remove('estimator')
        columns = ['estimator']+columns
        df = df[columns]
        return df
      
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC

models_list = { 
    'ExtraTreesClassifier': ExtraTreesClassifier(),
    'RandomForestClassifier': RandomForestClassifier(),
}

params_list = { 
    'ExtraTreesClassifier': {
        'n_estimators': np.arange(100, 3000, 100, dtype=int)
        },
    'RandomForestClassifier': {
        'criterion': ['gini', 'entropy'],
        'n_estimators': [8, 16]
        },
}


helper1 = EstimatorSelectionHelper(models_list, params_list)
helper1.fit(X_train_genetic_disorder_scaled, y_train_genetic_disorder, scoring='f1_weighted', n_jobs=-1)
helper1.score_summary()
