from distutils.core import setup

setup(name='DatacleaningD3MWrapper',
    version='1.1.0',
    description='A wrapper for running the punk datacleaning functions in the d3m environment.',
    packages=['DatacleaningD3MWrapper'],
    install_requires=["numpy",
        "pandas",
        "requests",
        "typing",
        "punk==3.0.0"],
    dependency_links=[
    ],
    entry_points = {
        'd3m.primitives': [
            'distil.datacleaning = DatacleaningD3MWrapper:datacleaning'
        ],
    },
)
