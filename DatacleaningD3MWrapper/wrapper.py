import os.path
import numpy as np
import pandas
import pickle
import requests
import ast
import typing
from json import JSONDecoder
from typing import List

from punk.preppy import CleanStrings, CleanDates, CleanNumbers
from d3m.primitive_interfaces.base import PrimitiveBase, CallResult

from d3m import container, utils
from d3m.metadata import hyperparams, base as metadata_base, params

__author__ = 'Distil'
__version__ = '3.0.0'

Inputs = container.pandas.DataFrame
Outputs = container.pandas.DataFrame

class Params(params.Params):
    pass


class Hyperparams(hyperparams.Hyperparams):
    pass

class datacleaning(PrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    metadata = metadata_base.PrimitiveMetadata({
        # Simply an UUID generated once and fixed forever. Generated using "uuid.uuid4()".
        'id': "fc6bf33a-f3e0-3496-aa47-9a40289661bc",
        'version': __version__,
        'name': "Data cleaning",
        # Keywords do not have a controlled vocabulary. Authors can put here whatever they find suitable.
        'keywords': ['Clean data values in data frame'],
        'source': {
            'name': __author__,
            'uris': [
                # Unstructured URIs.
                "https://github.com/NewKnowledge/datacleaning-d3m-wrapper",
            ],
        },
        # A list of dependencies in order. These can be Python packages, system packages, or Docker images.
        # Of course Python packages can also have their own dependencies, but sometimes it is necessary to
        # install a Python package first to be even able to run setup.py of another package. Or you have
        # a dependency which is not on PyPi.
         'installation': [{
            'type': metadata_base.PrimitiveInstallationType.PIP,
            'package_uri': 'git+https://github.com/NewKnowledge/datacleaning-d3m-wrapper.git@{git_commit}#egg=DatacleaningD3MWrapper'.format(
                git_commit=utils.current_git_commit(os.path.dirname(__file__)),
            ),
        }],
        # The same path the primitive is registered with entry points in setup.py.
        'python_path': 'd3m.primitives.distil.datacleaning',
        # Choose these from a controlled vocabulary in the schema. If anything is missing which would
        # best describe the primitive, make a merge request.
        'algorithm_types': [
            metadata_base.PrimitiveAlgorithmType.DATA_STRUCTURE_ALIGNMENT,
        ],
        'primitive_family': metadata_base.PrimitiveFamily.DATA_CLEANING,
    })
    
    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0)-> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed)
                
        self._decoder = JSONDecoder()
        self._params = {}

    def fit(self) -> None:
        pass
    
    def get_params(self) -> Params:
        return self._params

    def set_params(self, *, params: Params) -> None:
        self.params = params

    def set_training_data(self, *, inputs: Inputs, outputs: Outputs) -> None:
        pass
        
    def produce(self, *, inputs: Inputs, timeout: float = None, iterations: int = None) -> CallResult[Outputs]:
        """
        Produce primitive's best guess for the structural type of each input column.
        
        Parameters
        ----------
        inputs : Input pandas frame

        Returns
        -------
        Outputs
            The outputs is two lists of lists, each has length equal to number of columns in input pandas frame. 
            Each entry of the first one is a list of strings corresponding to each column's multi-label classification.
            Each entry of the second one is a list of floats corresponding to prediction probabilities.
        """
        
        """ Accept a pandas data frame, predicts column types in it
        frame: a pandas data frame containing the data to be processed
        -> a list of two lists of lists of 1) column labels and then 2) prediction probabilities
        """
        
        string_cleaner = CleanStrings()
        number_cleaner = CleanNumbers()
        date_cleaner = CleanDates()

        def dtype_apply(series):
            if series.dtype in ['int64', 'float64']:
                return number_cleaner.clean_numbers(series)
            elif series.dtype in ['object']:
                return string_cleaner.clean_strings(series)
            elif 'datetime' in series.dtype:
                return date_cleaner.clean_dates(series)
            else: 
                return series

        try:
            return inputs.apply(dtype_apply)
        except:
            return inputs


if __name__ == '__main__':
    client = datacleaning(hyperparams={})
    # make sure to read dataframe as string!
    # frame = pandas.read_csv("https://query.data.world/s/10k6mmjmeeu0xlw5vt6ajry05",dtype='str')
    frame = pandas.read_csv("https://s3.amazonaws.com/d3m-data/merged_o_data/o_4550_merged.csv",dtype='str')
    result = client.produce(inputs = frame)
    print(result)
