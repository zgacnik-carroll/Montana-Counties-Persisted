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

def load_city_data(filename):
    """
    Loads known cities from a text file.

    Returns:
        dict: city_name(lowercase) -> license_prefix
    """
    cities = {}

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                city, prefix = line.strip().split(",")
                cities[city.lower()] = int(prefix)
    except FileNotFoundError:
        # File will be created later if it does not exist
        pass

    return cities

def add_city_to_store(filename, city, prefix):
    """
    Appends a new city to the persistent data store.
    """
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"{city},{prefix}\n")

def license_lookup(counties):
    """Lookup county by license plate prefix."""
    prefix = int(input("Enter license plate prefix: "))

    if prefix in counties:
        county, seat = counties[prefix]
        print(f"County: {county}")
        print(f"County Seat: {seat}")
    else:
        print("Unknown license plate prefix.")

def city_lookup(cities, counties, city_file):
    """Lookup license prefix by city name."""
    city = input("Enter city name: ").lower()

    if city in cities:
        prefix = cities[city]
        county, _ = counties[prefix]
        print(f"County: {county}")
        print(f"License Prefix: {prefix}")
    else:
        print("City not found.")
        prefix = int(input("Enter license prefix for this city: "))

        # Store persistently
        add_city_to_store(city_file, city, prefix)

        # Update in-memory dictionary
        cities[city] = prefix

        print("City added for future lookups.")

def main():
    counties = load_county_data("MontanaCounties.csv")
    cities = load_city_data("cities.txt")

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
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()