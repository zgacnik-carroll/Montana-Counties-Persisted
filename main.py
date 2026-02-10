"""
main.py

Author: Zack Gacnik
Description:
    This program allows users to look up Montana counties using
    license plate prefixes or city names. County data is loaded
    from a CSV file, while user-added city mappings are stored
    persistently in a text file.

    Features:
    - Lookup county and county seat by license plate prefix.
    - Lookup license plate prefix by city name.
    - Persistently store new city entries for future use.
    - Basic input validation and error handling.

Requirements:
    Python 3.13
"""

import csv

def load_county_data(filename):
    """
    Load county data from a CSV file into a dictionary.

    The CSV file must contain the following columns:
        - License Plate Prefix
        - County
        - County Seat

    Args:
        filename (str): Path to the CSV file containing county data.

    Returns:
        dict[int, tuple[str, str]]:
            A dictionary mapping license plate prefixes to a tuple
            containing (county_name, county_seat).
    """
    counties = {}

    # Open CSV file and read rows as dictionaries.
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Convert prefix to integer for faster lookup and validation.
            prefix = int(row["License Plate Prefix"])

            # Store county information as a tuple.
            counties[prefix] = (row["County"], row["County Seat"])

    return counties

def load_city_data(filename):
    """
    Load known city-to-prefix mappings from a text file.

    Each line in the file must follow this format:
        city_name,prefix

    City names are stored in lowercase to allow
    case-insensitive lookups.

    Args:
        filename (str): Path to the city data file.

    Returns:
        dict[str, int]:
            Dictionary mapping city names (lowercase)
            to license plate prefixes.
    """
    cities = {}

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                # Remove whitespace and newline characters.
                line = line.strip()

                # Skip empty lines to avoid parsing errors.
                if not line:
                    continue

                try:
                    # Split line into city and prefix.
                    city, prefix = line.split(",")

                    # Store using lowercase keys for consistency.
                    cities[city.lower()] = int(prefix)

                except ValueError:
                    # Ignore malformed lines instead of crashing.
                    continue

    except FileNotFoundError:
        # File may not exist on first run; this is acceptable.
        pass

    return cities

def populate_county_seats(cities, counties):
    """
    Add county seats to the city lookup dictionary.

    This allows county seats from the CSV file to be recognized
    automatically as valid city inputs without requiring them
    to be stored in the persistent city file.
    """
    for prefix, (_, seat) in counties.items():
        seat_lower = seat.lower()

        # Do not overwrite user-added entries.
        if seat_lower not in cities:
            cities[seat_lower] = prefix

def add_city_to_store(filename, city, prefix):
    """
    Append a new city and prefix mapping to the data file.

    This allows newly added cities to persist between program runs.

    Args:
        filename (str): Path to the city data file.
        city (str): Name of the city.
        prefix (int): Associated license plate prefix.
    """
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"{city},{prefix}\n")

def license_lookup(counties):
    """
    Perform a lookup using a license plate prefix.

    Prompts the user for a numeric prefix and displays
    the associated county and county seat if found.

    Args:
        counties (dict): Mapping of prefixes to county data.
    """

    # Loop allows user to retry without returning to main menu.
    while True:
        user_input = input(
            "\nEnter license plate prefix (or 'q' to return): "
        )

        if user_input.lower() == "q":
            return

        try:
            prefix = int(user_input)
        except ValueError:
            print("Please enter a valid number.")
            continue

        # Check whether the prefix exists in the dataset.
        if prefix in counties:
            county, seat = counties[prefix]
            print(f"County: {county}")
            print(f"County Seat: {seat}")
        else:
            print("Unknown license plate prefix.")

def city_lookup(cities, counties, city_file):
    """
    Perform a lookup using a city name.

    If the city exists, the associated county and prefix
    are displayed. If not, the user is prompted to add the
    city to the persistent data store.

    Args:
        cities (dict): City-to-prefix mapping.
        counties (dict): Prefix-to-county mapping.
        city_file (str): Path to persistent city storage file.
    """

    # Loop allows user to retry without returning to main menu.
    while True:
        city = input(
            "\nEnter city name (or 'q' to return): "
        ).lower()

        # Prevent empty input.
        if city == "q":
            return

        if not city:
            print("City name cannot be empty.")
            continue

        # Existing city lookup.
        if city in cities:
            prefix = cities[city]
            county, _ = counties[prefix]
            print(f"County: {county}")
            print(f"License Prefix: {prefix}")
            continue

        print("City not found.")

        # Allow user to add new mapping.
        try:
            prefix = int(
                input("Enter license prefix for this city (or -1 to cancel): ")
            )
        except ValueError:
            print("Invalid prefix.")
            continue

        if prefix == -1:
            continue

        # Validate that prefix exists in county data.
        if prefix not in counties:
            print("That license prefix does not exist.")
            continue

        # Persist new entry and update in-memory dictionary.
        add_city_to_store(city_file, city, prefix)
        cities[city] = prefix

        print("City added for future lookups.")

def main():
    """
    Main program loop.

    Loads required data files and repeatedly prompts the
    user for an action until the user chooses to quit.
    """
    counties = load_county_data("MontanaCounties.csv")
    cities = load_city_data("cities.txt")

    # Automatically add county seats as valid city entries.
    populate_county_seats(cities, counties)

    while True:
        print("\nSelect an option:")
        print("1 - Lookup by license plate prefix")
        print("2 - Lookup by city")
        print("3 - Quit")

        choice = input("Enter choice: ")

        if choice == "1":
            license_lookup(counties)

        elif choice == "2":
            city_lookup(cities, counties, "cities.txt")

        elif choice == "3":
            print("Thanks for playing. Goodbye!")
            break

        else:
            print("Invalid choice.")

# Standard Python entry point check.
# Ensures main() only runs when the file is executed directly.
if __name__ == "__main__":
    main()
