FROM python:slim

# Upgrade the packages
RUN apt-get update && apt-get -y upgrade

# Install the C compiler and required OS programs
RUN apt-get install -y curl gcc g++ zlib1g-dev vim lbzip2
RUN apt-get install -y build-essential python3-dev python3-dev python3-setuptools
RUN apt-get install -y python3-numpy python3-scipy libatlas-base-dev libatlas3-base
RUN apt-get install -y gfortran libopenblas-dev libopenblas-base pkg-config libopenblas64-dev
RUN  export BLAS=/usr/lib/x86_64-linux-gnu/libopenblas.a

# Create a working directory
RUN mkdir /experiment

# Install the required Python libraries
COPY requirements.txt /opt/
RUN pip install -r /opt/requirements.txt

# Install Codon
RUN curl https://exaloop.io/install.sh > codon_install.sh
RUN chmod u+x codon_install.sh
RUN ./codon_install.sh

# Install PyPy
RUN curl https://downloads.python.org/pypy/pypy3.9-v7.3.11-linux64.tar.bz2 > pypy3.9-v7.3.11-linux64.tar.bz2
RUN tar xf pypy3.9-v7.3.11-linux64.tar.bz2

# Make a virtual environment for PyPy
RUN cd /experiment
RUN virtualenv -p /pypy3.9-v7.3.11-linux64/bin/pypy my-pypy-env
RUN my-pypy-env/bin/pypy -mpip install -r /opt/requirements.txt

# Copy the src files
COPY src/ /experiment

# Set the working directory
WORKDIR /experiment