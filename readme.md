# Codon experiment

## Introduction to Codon

Codon is a compiler that generates machine code from code that is syntactically similar to Python. It is not a direct replacement for Python's interpreter as some modules are not implemented (such as `csv`). Its performance is claimed to be on par with C/C++ and it supports native multithreading and is garbage-collected (https://docs.exaloop.io/codon/). Codon is licensed under Business Source Licence (BSL), which means it is free for non-production use.

To assess its performance capabilities, a Docker image was made containing the latest version of Codon (v0.15) and Python (v3.11.2) to perform a data extraction task. A Python script created a CSV file with 1 million rows of synthetic data consisting of a phone number field and a free-text message field that may contain a vehicle registration (VRN). Three experiments were performed:

1. Read the CSV file (without performing any processing of its contents);
2. Read the CSV file and standardise the phone number field to create an internationalised number;
3. Read the CSV file and extract VRNs from the free-text field using a regular expression.

A Bash script ran each experiment five times and execution times were calculated using the Linux tool `time`.

Execution times (in seconds) for the experiments using Python code were:

| Experiment | 1      | 2      | 3      | 4      | 5      | Mean   |
| ---------- | ------ | ------ | ------ | ------ | ------ | ------ |
| 1          | 3.007  | 3.248  | 3.324  | 3.357  | 2.886  | 3.164  |
| 2          | 92.444 | 94.476 | 98.737 | 88.438 | 87.995 | 92.418 |
| 3          | 16.579 | 17.387 | 16.686 | 16.974 | 16.445 | 16.814 |

Execution times (in seconds) for the experiments using Codon were:

| Experiment | 1       | 2       | 3      | 4      | 5      | Mean    |
| ---------- | ------- | ------- | ------ | ------ | ------ | ------- |
| 1          | 6.183   | 6.348   | 5.898  | 6.078  | 6.091  | 6.120   |
| 2          | 118.304 | 108.363 | 96.183 | 99.474 | 95.368 | 103.538 |
| 3          | 8.382   | 8.462   | 8.348  | 8.292  | 7.257  | 8.148   |

The mean experimental result times are summarised in the table below:

| Experiment | Description               | Python | Codon   |
| ---------- | ------------------------- | ------ | ------- |
| 1          | Reading a file            | 3.164  | 6.120   |
| 2          | Standardise phone numbers | 92.418 | 103.538 |
| 3          | Extract VRNs              | 16.814 | 8.148   |

The fact that Codon is not a drop-in replacement for Python became apparent when the in-built Python module `csv` could not be used to read the synthetic dataset. A check for the existence of a file using `os.path.exists()` would not compile using Codon. Additionally, a minor change of `import phonenumbers` to `from python import phonenumbers` was required for Codon.

The conclusion of the experiment is that Codon was slower than Python at reading a CSV file and also slower at executing code in the `phonenumbers` Python library. To get the speed improvement claimed the Python library dependencies would probably have to be coded in Codon. However, it was much faster at computing regular expressions. Codon's license is potentially too restrictive for wide-spread adoption in industry.

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