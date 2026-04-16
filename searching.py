from pathlib import Path
import json

def read_data(file_name, field):
    """
    Reads a JSON file and returns data for a given field.

    Args:
        file_name (str): Name of the JSON file.
        field (str): Key to retrieve from the JSON data.
            Must be one of: 'unordered_numbers', 'ordered_numbers' or 'dna_sequence'.

    Returns:
        list | str | None:
            - list: If data retrieved by the selected field contains numeric data.
            - str: If field is 'dna_sequence'.
            - None: If the field is not supported.
    """
    allowed_fields = ["unordered_numbers", "ordered_numbers", "dna_sequence"]

    if field not in allowed_fields:
        return None

    file_path = Path(__file__).resolve().parent / file_name

    with file_path.open("r", encoding="utf-8") as file_handle:
        data = json.load(file_handle)

    if field not in data:
        return None

    return data[field]


def linear_search(sequence, target):
    positions = []
    index = 0

    while index < len(sequence):
        if sequence[index] == target:
            positions.append(index)
        index += 1

    result = {
        "positions": positions,
        "count": len(positions)
    }

    return result


def main():
    sequential_data = read_data("sequential.json", "unordered_numbers")
    searched_number = 5

    print(sequential_data)
    print(linear_search(sequential_data, searched_number))


if __name__ == "__main__":
    main()

