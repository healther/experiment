Travis CI Status [![Build Status](https://travis-ci.org/healther/experiment.svg)](https://travis-ci.org/healther/experiment)
# experiment
This [repository](https://github.com/healther/experiment)  contains a tool to generate experiments for parameter studies.
It was written as part of my PhD work in the year 2017, if you stumble over it, feel free to use it. 
Any feedback is very welcome, feel free to open an issue or email me. 

A parameter study for the purposes of this tool is a number of free parameters for each of which you have a list of possible values and you want to test all combinations of these.
The idea is that each simulation is uniquely defined by a configuration file (which contains at least all parameters that are to be varied, but may use more).
This tool generates these configuration files from a template and is then able to submit the simulations to a scheduler and run all of these on a HPC-cluster.

An example of such a generation file is `test.yaml`.
There are essentially three parts of this file: 
  * execution parameters
  * the configuration template
  * replacements

### Execution parameters

these are handed down to the scheduler and package the simulations such that each jobs runtime will be smaller than `walltime`, given that each simulation takes `timeperjob` seconds. 
Implemented are the handling on the [BWNemo cluster](https://www.bwhpc-c5.de/wiki/index.php/Category:BwForCluster_NEMO), but it should be relatively straight forward to implement it for different clusters.

### Configuration template

everything below `stub` is going to be handed (as the first command line argument) to the `executable`, when being called by the executor.
In the end `executable` should put an `analysis` file in the working folder that contains the relevant results.
`experiment.py` can collect these with the `--summarize`-flag.

### Replacements

these are the lists for the single parameters that should be combined.
The keys are arbitrary strings that are placed as a value in `stub` and replaced by all combinations.
Each key may appear multiple times in `stub` and for each realization all appearances will be replaced with the same value.

The simulations are created in the `simulations/$experimentName` sub folder and a copy of the executed simulation file is placed in `simulations/01_runs/$experimentName` for later comparisons.
