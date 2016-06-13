# RWR_FOR_ALGO
## Introduction
This project is mainly for the algorithm final test. It contains two applications, namely Entity Linking and Reweighted Random Walks Method. Entity linking is written by Python. RRWM is written by Matlab. 
The contribution of EL is for its online scrapping and lightweight implementation. Also it contains several testcases for your convienience. For the data analysis you should see the thesis.
The contribution of RRWM is image matching. It improves the work by the method of parameter optimization.
For more detail, please review the thesis.
## Organisation
* algo: the implementaion foundation of the random walk algorithm
* paper directory: some paper references for reading
* doc: some online content
* test: the functional test directory
* spider: the implementation to scrap content from wiki
* util: other utility functions
* thesis: our paper work
* app: the implementation of EL
* rrwr: the implementation of RRWR

## Installation
The EL project is mainly written in Python, you need to install several packages.
Later on, I will write the package egg for it. However, not now.
* networkx
* pydot
* metis
* numpy
* scipy
* scrapy


## Bug
It may have some bugs to track on:
* the wiki content linking.
* when the graph is not inversable which rarely is the case
