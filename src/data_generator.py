import csv
import numpy as np
import random
import string
import sys

from faker import Faker
fake = Faker()


def generate_uk_phone_number():
    """Generate a phone number based in the UK."""
    formats = [
        "(01xx xx) xx xxx",
        "(01xxx) xxx xxx",
        "(01x1) xxx xxxx",
        "(011x) xxx xxxx",
        "(02x) xxxx xxxx",
        "03xx xxx xxxx",
        "055 xxxx xxxx",
        "056 xxxx xxxx",
        "07x xxxx xxxx",
        "07xxx xxx xxx",
        "0800 xxx xxxx",
        "08xx xxx xxxx",
        "09xx xxx xxxx",
        "(0169 77) xxxx",
        "(01xxx) xx xxx",
        "0800 xxx xxx",
        "0800 11 11",
        "0845 46 4x"
    ]

    # Randomly select one of the formats
    fmt = random.choice(formats)

    # Replace each 'x' character with a random digit
    phone = [c if c != 'x' else str(random.randint(0, 9)) for c in fmt]

    # Return a string
    return "".join(phone)


def generate_vrn():
    """Generate a random UK VRN."""

    letters = string.ascii_uppercase
    numbers = "0123456789"

    return "".join([
        random.choice(letters),
        random.choice(letters),
        random.choice(numbers),
        random.choice(numbers),
        " ",
        random.choice(letters),
        random.choice(letters),
        random.choice(letters)]
    )


def generate_tokens(num_tokens):
    """Generate num_tokens random tokens of text."""

    tokens = []
    while len(tokens) < num_tokens:
        tokens.extend(fake.paragraph(nb_sentences=1)[:-1].split(" "))

    return tokens[:num_tokens]


def random_text(poisson_lambda, p_vrn):
    """Generate random text with a Poisson distributed length."""

    assert poisson_lambda > 0, f"Mean of the number of tokens must be positive"
    assert 0.0 <= p_vrn <= 1.0, f"Probability of a VRN occurring must be in the range [0,1]"

    num_tokens = np.random.poisson(poisson_lambda)

    # Ensure there is a minimum of 1 token
    num_tokens = max(1, num_tokens)
    tokens = generate_tokens(num_tokens)

    vrn_present = np.random.binomial(1, p_vrn)
    if vrn_present:
        # Randomly select a token to replace with a VRN
        tokens[random.randint(0, len(tokens)-1)] = generate_vrn()

    return " ".join(tokens)


def generate_row(poisson_lambda, p_vrn):
    """Generate a row of synthetic data."""

    return {
        "Phone_number": generate_uk_phone_number(),
        "Message": random_text(poisson_lambda, p_vrn)
    }


def generate_dataset(output_filepath, num_rows, poisson_lambda, p_vrn):
    """Generate a dataset with num_rows rows and save to output_filepath."""

    with open(output_filepath, 'w', newline='') as fp:
        fieldnames = ['Phone_number', 'Message']
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()

        for _ in range(num_rows):
            writer.writerow(generate_row(poisson_lambda, p_vrn))


if __name__ == '__main__':

    # Number of rows of data to generate
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <number of rows>")
        sys.exit(-1)

    num_rows = int(sys.argv[1])

    # Location for the output CSV file
    output_filepath = "./dataset.csv"

    # Parameters of probability distributions
    poisson_lambda = 10  # Mean number of tokens in a message
    p_vrn = 0.2          # Probability of a VRN occurring in a message

    # Generate the dataset
    generate_dataset(output_filepath, num_rows, poisson_lambda, p_vrn)
    print(f"Dataset written to {output_filepath} with {num_rows} rows of data")
