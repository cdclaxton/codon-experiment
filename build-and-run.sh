#!/bin/bash
docker image build -t codon-experiment:latest .
docker container run -it codon-experiment:latest /bin/bash