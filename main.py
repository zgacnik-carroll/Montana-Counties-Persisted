import csv

def load_county_data(filename):
    """
    Loads county data from CSV into a dictionary.

    Returns:
        dict: license_prefix -> (county_name, county_seat)
    """
    counties = {}

    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            prefix = int(row["License Plate Prefix"])
            counties[prefix] = (row["County"], row["County Seat"])

    return counties