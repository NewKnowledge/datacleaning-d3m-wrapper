# Datacleaning D3M Wrapper
Wrapper of a data cleaning primitive (the base libraries can be found here: https://github.com/NewKnowledge/punk) into D3M infrastructure. All code is written in Python 3.5 and must be run in 3.5 or greater. 

## Install

pip3 install -e git+https://github.com/NewKnowledge/datacleaning-d3m-wrapper.git#egg=DatacleaningD3MWrapper --process-dependency-links

## Output
The output is a frame structurally identical to the input frame, with each feature cleaned according to its type (e.g. all date objects will be modified to be of a common structure).

## Available Functions

#### produce
Perform basic cleaning operations on the data, including enforcing consistency of data and properly handling missing values. The input is an input pandas frame. The output is a frame structurally identical to the input frame, with each feature cleaned according to its type (e.g. all date objects will be modified to be of a common structure).
