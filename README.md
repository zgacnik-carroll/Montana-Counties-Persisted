# Montana License Plate County Lookup - Persisted

## Description

This program allows users to look up Montana counties using either a
license plate prefix or a city name. County information is loaded from
a CSV file, and city-to-prefix mappings are stored persistently so that
newly added cities are remembered between program runs.

---

## Requirements

- Python **3.13**

You can check your Python version with:

```bash
python --version
```

---

## How to Run

1. Clone this repository within your desired directory.
2. Open a terminal in that project directory.
3. Run the program:

```bash
python main.py
```

---

## Program Usage

After starting the program, you will see a menu:

```
1 - Lookup by license plate prefix
2 - Lookup by city
3 - Quit
```

### Lookup by License Plate Prefix
- Enter a numeric license plate prefix.
- The program displays the corresponding county and county seat.

### Lookup by City
- Enter a city name.
- If the city exists, the program displays the associated county and prefix.
- If the city is not found, you may add it for future use.

New cities are automatically saved to `cities.txt`.

---

## Data Files

### MontanaCounties.csv
Contains official county data including:
- License Plate Prefix
- County Name
- County Seat

### cities.txt
Stores user-added city mappings in the format:

```
city_name,prefix
```

This file is automatically updated by the program.

Have fun discovering counties and adding city data for the
beautiful state of Montana!
