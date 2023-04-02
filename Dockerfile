FROM python:slim

# Upgrade the packages
RUN apt-get update && apt-get -y upgrade

# Install the C compiler and required OS programs
RUN apt-get install -y curl gcc g++ zlib1g-dev vim

# Create a working directory
RUN mkdir /experiment

# Install the required Python libraries
COPY requirements.txt /opt/
RUN pip install -r /opt/requirements.txt

# Install Codon
RUN curl https://exaloop.io/install.sh > codon_install.sh
RUN chmod u+x codon_install.sh
RUN ./codon_install.sh

# Copy the src files
COPY src/ /experiment

# Set the working directory
WORKDIR /experiment