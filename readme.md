# Codon experiment

## Introduction to Codon

Codon is a compiler that generates machine code from code that is syntactically similar to Python. It is not a direct replacement for Python's interpreter as some modules are not implemented (such as `csv`). Its performance is claimed to be on par with C/C++ and it supports native multithreading and is garbage-collected (https://docs.exaloop.io/codon/). Codon is licensed under Business Source Licence (BSL), which means it is free for non-production use.

To assess its performance capabilities, a Docker image was made containing the latest version of Codon (v0.15), the CPython interpreter (v3.11.2) and the PyPy interpreter (v7.3.11) to perform a data extraction task. A Python script created a CSV file with synthetic data consisting of a phone number field and a free-text message field that may contain a vehicle registration (VRN). Four experiments were performed:

1. Read the CSV file (without performing any processing of its contents);
2. Read the CSV file and standardise the phone number field to create an internationalised number;
3. Read the CSV file and extract VRNs from the free-text field using a regular expression;
4. Read the CSV file and train a Support Vector Machine (SVM) to predict whether a VRN is present in a message.

Experiments 1, 2 and 3 processed a dataset of 1 million rows, but experiment 4 had a smaller dataset of 100,000 rows due to the computational complexity of running the machine learning.

A Bash script ran each experiment five times and execution times were calculated using the Linux tool `time`.

Execution times (in seconds) for the experiments using the standard CPython interpreter were:

| Experiment | Run 1  | Run 2  | Run 3  | Run 4  | Run 5  | Mean   |
| ---------- | ------ | ------ | ------ | ------ | ------ | ------ |
| 1          | 3.007  | 3.248  | 3.324  | 3.357  | 2.886  | 3.164  |
| 2          | 92.444 | 94.476 | 98.737 | 88.438 | 87.995 | 92.418 |
| 3          | 16.579 | 17.387 | 16.686 | 16.974 | 16.445 | 16.814 |
| 4          | 342.99 | 353.44 | 318.38 | 284.55 | 294.75 | 318.82 |

Execution times (in seconds) for the experiments using the Codon compiler were:

| Experiment | Run 1   | Run 2   | Run 3  | Run 4  | Run 5  | Mean    |
| ---------- | ------- | ------- | ------ | ------ | ------ | ------- |
| 1          | 6.183   | 6.348   | 5.898  | 6.078  | 6.091  | 6.120   |
| 2          | 118.304 | 108.363 | 96.183 | 99.474 | 95.368 | 103.538 |
| 3          | 8.382   | 8.462   | 8.348  | 8.292  | 7.257  | 8.148   |
| 4          | 290.95  | 284.66  | 281.31 | 280.93 | 281.17 | 283.80  |

Execution times (in seconds) for the experiments using the PyPy interpreter were:

| Experiment | Run 1  | Run 2  | Run 3  | Run 4  | Run 5  | Mean   |
| ---------- | ------ | ------ | ------ | ------ | ------ | ------ |
| 1          | 4.494  | 4.970  | 3.512  | 5.336  | 5.901  | 4.843  |
| 2          | 43.311 | 34.124 | 30.609 | 37.604 | 35.843 | 36.298 |
| 3          | 12.797 | 10.301 | 13.441 | 11.057 | 13.180 | 12.155 |
| 4          | 243.21 | 265.27 | 292.92 | 280.05 | 281.02 | 272.49 |

The mean experimental result times are summarised in the table below:

| Experiment | Description                     | Mean time in CPython (s) | Mean time in Codon (s) | Mean time in PyPy (s) | Codon speed up | PyPy speed up |
| ---------- | ------------------------------- | ------------------------ | ---------------------- | --------------------- | -------------- | ------------- |
| 1          | Reading a file                  | 3.164                    | 6.120                  | 4.843                 | Slower         | Slower        |
| 2          | Standardise phone numbers       | 92.418                   | 103.538                | 36.298                | Slower         | 2.5 times     |
| 3          | Extract VRNs                    | 16.814                   | 8.148                  | 12.155                | 2.1 times      | 1.4 times     |
| 4          | ML to predict presence of a VRN | 318.82                   | 283.80                 | 272.49                | 1.1 times      | 1.2 times     |

The fact that Codon is not a drop-in replacement for Python became apparent when the in-built Python module `csv` could not be used to read the synthetic dataset. A check for the existence of a file using `os.path.exists()` would not compile using Codon. Additionally, a minor change of `import phonenumbers` to `from python import phonenumbers` was required for Codon.

The conclusion of the experiment is that Codon was slower than CPython at reading a CSV file and also slower at executing code in the `phonenumbers` Python library. However, it was 2.1 times faster at the task of performing regular expression matching on text and 1.1 times faster at training a SVM with Scikit-learn. Codon's license is potentially too restrictive for wide-spread adoption in industry though. By contrast, PyPy's performance and license make it a more attractive solution at present.

## Create a Docker image and run a test case

```bash
# Build the Docker image
docker image build -t codon-experiment:latest .

# Run the Docker container to inspect it
docker container run -it codon-experiment:latest /bin/bash

# Build a test executable and run
/root/.codon/bin/codon build /experiment/fib.py
./fib
```

## Run experiments

```bash
./build-and-run.sh

# Once the Docker container's shell loads, type
./run-experiments.sh
```

## Issues found

- `error: no module named 'csv'` -- This occurred with `import csv` as the `csv` module has not been ported yet.
- `error: cannot import name 'path' from 'os.__init__'` -- This occurred with the line `os.path.exists()`.
- `error: 'File' object has no attribute 'readline'` -- Method `readline` hasn't been ported as can be seen from https://github.com/exaloop/codon/blob/develop/stdlib/internal/file.codon
- Ran command to build and run the executable and got the following error message:

```bash
CError: libpython.so: cannot open shared object file: No such file or directory

Raised from: std.internal.dlopen.dlopen.2:0
/root/.codon/lib/codon/stdlib/internal/dlopen.codon:31:9

Backtrace:
  [0x401ad5] std.internal.dlopen.dlopen.2:0[str,int].231 at /root/.codon/lib/codon/stdlib/internal/dlopen.codon:31
  [0x405637] std.internal.python.setup_python:0[bool].629 at /root/.codon/lib/codon/stdlib/internal/python.codon
  [0x4056a3] std.internal.python.ensure_initialized:0[bool].639 at /root/.codon/lib/codon/stdlib/internal/python.codon:361
  [0x406677] pyobj._import:0[str].747 at /root/.codon/lib/codon/stdlib/internal/python.codon:360
  [0x413eb8] main.0 at /experiment/run_experiment_codon.py:2
Aborted (core dumped)
```

The solution was to run `export CODON_PYTHON=/usr/local/lib/libpython3.so`

- `1 * (len(extract_vrns(row['Message'])) > 0)` generated an error `error: unsupported operand type(s) for *: 'int' and 'bool'`
