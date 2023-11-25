import pandas as pd

from typing import List

from datetime import datetime

import matplotlib.pyplot as plt

from scipy import stats


class Dataset:
    def __init__(self, data : pd.DataFrame, store_dataset_versions=False):
        self.curr_v = data # current version of dataset
        
        self._store_dataset_versions = store_dataset_versions

        self._err_sdv_msg = "Storing of dataset's versions isn't available."
    
        if self._store_dataset_versions:
            self._dataset_versions = {
                'initial' : data,
            }

        self.statistics_df = pd.DataFrame(
            {'Columns' : self.curr_v.columns}
        )


    ##### Version control system #####

    def get_versions_list(self):
        """
        Return available versions if store_dataset_versions is True.
        None otherwise.
        """
        assert self._store_dataset_versions, self._err_sdv_msg
        
        return self._dataset_versions.keys()

    
    def save_version(self, saving_name=None):
        assert self._store_dataset_versions, self._err_sdv_msg

        if not saving_name:
            saving_name = str(datetime.now().replace(microsecond=0))
        
        assert type(saving_name) == str, 'Incorrect saving name type.'
        
        self._dataset_versions[saving_name] = self.curr_v

    
    def load_version(self, version, save_curr=False, saving_name=None):
        assert self._store_dataset_versions, self._err_sdv_msg
        
        assert version in self._dataset_versions.keys(), "No version with this name found."

        if save_curr:
            self.save_version(saving_name=saving_name)

        self.curr_v = self._dataset_versions['version']


    ##### General info about dataset #####

    def info(self):
        return self.curr_v.info()

    
    def head(self, n=5):
        return self.curr_v.head(n=n)
    

    def desribe(self):
        return self.curr_v.describe()


    ##### NaN values handling #####
    
    def isna_statistics(self, del_threshold=0.45, print_results=True):
        isna_count = self.curr_v.isna().sum().values # Count of nan values for each column

        self.statistics_df['Isna count'] = isna_count
        self.statistics_df['Percentage of NaN'] = isna_count / len(self.curr_v)

        self._cols_to_del = self.statistics_df[ \
            self.statistics_df["Percentage of NaN"] > del_threshold \
            ].sort_values(by='Percentage of NaN', ascending=False)["Columns"].values

        if print_results:
            print(self.statistics_df[self.statistics_df['Isna count'] > 0].sort_values(by='Percentage of NaN', ascending=False), end = '\n\n')
            print(f'Recommended to delete following columns: {self._cols_to_del}')

    
    def isna_delete(self):
        """
        Deletes columns with percentage of NaN greater than setted threshold, 
        that were found by isna_statistics method.

        If isna_statistics method wasn't called, then calls without results printing
        and deletes the given columns.

        If _store_dataset_versions is True, saved the version before deleting.

        """
        if self._store_dataset_versions:
            self._dataset_versions['before_nan_del'] = self.curr_v

        try:
            self._cols_to_del
        
        except AttributeError:
            self.isna_statistics(print_results=False)
        
        self.curr_v = self.curr_v.drop(self._cols_to_del, axis=1)

    
    def isna_replace(self, cols: List[str], strategy='median'):
        pass


    ##### Visualizing #####


    def hist(self, col: str):
        plt.hist()