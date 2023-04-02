#!/bin/bash

# Build the executable using Codon
echo Building executable using Codon
/root/.codon/bin/codon build /experiment/run_experiment_codon.py

# Set the CODON_PYTHON environment variable to the Python shared library
export CODON_PYTHON=/usr/local/lib/libpython3.so

# Generate a dataset
# echo Generating dataset ...
# python data_generator.py 1000000

# Run Python experiments
TIMEFORMAT=%R
for i in {1..5}
do
    echo "Running Python experiments set $i"
    time python run_experiment.py 1;
    time python run_experiment.py 2;
    time python run_experiment.py 3;
    echo "---------------------------------"
done

# Run Codon experiments
for i in {1..5}
do
    echo "Running Codon experiments set $i"
    time ./run_experiment_codon 1;
    time ./run_experiment_codon 2;
    time ./run_experiment_codon 3;
    echo "---------------------------------"
done

# Generate a smaller dataset for the ML experiments
echo Generating dataset ...
python data_generator.py 100000

# Run Python experiments
for i in {1..5}
do
    echo "Running Python experiments set $i"
    time python run_experiment.py 4;
    echo "---------------------------------"
done

# Run Codon experiments
for i in {1..5}
do
    echo "Running Codon experiments set $i"
    time ./run_experiment_codon 4;
    echo "---------------------------------"
done