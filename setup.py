from distutils.core import setup

setup(name='DatacleaningD3MWrapper',
    version='3.01',
    description='A wrapper for running the punk datacleaning functions in the d3m environment.',
    packages=['DatacleaningD3MWrapper'],
    install_requires=["pandas==0.23.4",
        "punk==3.0.0"],
    dependency_links=[
    ],
    entry_points = {
        'd3m.primitives': [
            'data_cleaning.data_cleaning.Datacleaning = DatacleaningD3MWrapper:datacleaning'
        ],
    },
)
