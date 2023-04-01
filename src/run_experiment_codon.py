import os
from python import phonenumbers
import re
import sys

# VRN regex pattern
vrn_pattern = r"([A-Z]{2}[0-9]{2} [A-Z]{3})"
vrn_regex = re.compile(vrn_pattern, re.IGNORECASE)


def standardise_phonenumber(phone_number, default_country):
    """Standardise a single phonenumber."""

    # Preconditions
    assert isinstance(
        phone_number, str), f"Expected a str, got {type(phone_number)}"
    assert isinstance(default_country, str)

    # Parse the phone number
    try:
        number_obj = phonenumbers.parse(phone_number, default_country)
        std_number = phonenumbers.format_number(
            number_obj, phonenumbers.PhoneNumberFormat.E164)
        return std_number
    except:
        return None


def extract_vrns(text):
    """Extract VRNs from text."""
    return vrn_regex.findall(text)


def read_dataset(filepath):
    """Read a CSV dataset line-by-line."""

    with open(filepath) as fp:
        header = None
        for line in fp:
            if header is None:
                header = line.strip().split(",")
            else:
                parts = line.strip().split(",")
                yield dict(zip(header, parts))


def experiment_1(filepath):
    """Only read the input file."""
    num_rows = 0
    for row in read_dataset(filepath):
        num_rows += 1

    print(f"Read {num_rows} rows")


def experiment_2(filepath):
    """Read the input file and standardise the phone numbers."""
    num_rows = 0
    num_phonenumbers = 0

    for row in read_dataset(filepath):
        num_rows += 1
        phone_number = row['Phone_number']
        std = standardise_phonenumber(phone_number, 'GB')
        if std is not None:
            num_phonenumbers += 1

    print(f"Read {num_rows} rows")
    print(f"Standardised {num_phonenumbers} phone numbers")


def experiment_3(filepath):
    """Read the input file and extract VRNs."""

    num_rows = 0
    num_vrns = 0

    for row in read_dataset(filepath):
        num_rows += 1
        num_vrns += len(extract_vrns(row['Message']))

    print(f"Read {num_rows} rows")
    print(f"Extracted {num_vrns} VRNs")


if __name__ == '__main__':

    # Get the experiment number to run from the command line
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <experiment number>")
        sys.exit(-1)

    experiment = int(sys.argv[1])
    print(f"Running Codon experiment {experiment}")

    # Location of the dataset CSV file
    dataset_filepath = "./dataset.csv"

    # Run the experiment
    if experiment == 1:
        experiment_1(dataset_filepath)
    elif experiment == 2:
        experiment_2(dataset_filepath)
    elif experiment == 3:
        experiment_3(dataset_filepath)
    else:
        print(f"Unknown experiment: {experiment}")
