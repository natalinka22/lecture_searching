from pathlib import Path
import json
import time
import matplotlib.pyplot as plt
from generators import unordered_sequence

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


def binary_search(sequence, target):
    left = 0
    right = len(sequence) - 1

    while left <= right:
        middle = left + (right - left) // 2

        if sequence[middle] == target:
            return middle

        if sequence[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return None


def benchmark_searches():
    input_sizes = [100, 500, 1000, 5000, 10000]
    repetitions = 10
    linear_times = []
    binary_times = []

    for size in input_sizes:
        linear_total = 0.0
        binary_total = 0.0

        for _ in range(repetitions):
            unordered_data = unordered_sequence(size)
            ordered_data = sorted(unordered_data)
            target_value = unordered_data[size // 2]

            start_time = time.perf_counter()
            linear_search(unordered_data, target_value)
            linear_total += time.perf_counter() - start_time

            start_time = time.perf_counter()
            binary_search(ordered_data, target_value)
            binary_total += time.perf_counter() - start_time

        linear_times.append(linear_total / repetitions)
        binary_times.append(binary_total / repetitions)

    plt.figure(figsize=(8, 5))
    plt.plot(input_sizes, linear_times, marker="o", label="Linear search")
    plt.plot(input_sizes, binary_times, marker="o", label="Binary search")
    plt.title("Search time comparison")
    plt.xlabel("Input size")
    plt.ylabel("Average time (seconds)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("task4_search_benchmark.png")
    plt.close()

    return input_sizes, linear_times, binary_times


def pattern_search(sequence, pattern):
    positions = set()
    sequence_length = len(sequence)
    pattern_length = len(pattern)

    if pattern_length == 0:
        return positions

    start = 0

    while start <= sequence_length - pattern_length:
        pattern_index = 0
        match = True

        while pattern_index < pattern_length:
            if sequence[start + pattern_index] != pattern[pattern_index]:
                match = False
                break

            pattern_index += 1

        if match:
            positions.add(start)

        start += 1

    return positions


def main():
    sequential_data = read_data("sequential.json", "unordered_numbers")
    ordered_data = read_data("sequential.json", "ordered_numbers")
    dna_sequence = read_data("sequential.json", "dna_sequence")
    searched_number = 5
    ordered_searched_number = 14
    searched_pattern = "ATA"

    print(sequential_data)
    print(linear_search(sequential_data, searched_number))
    print(binary_search(ordered_data, ordered_searched_number))
    print(pattern_search(dna_sequence, searched_pattern))

    sizes, linear_times, binary_times = benchmark_searches()
    print(sizes)
    print(linear_times)
    print(binary_times)
    print("task4_search_benchmark.png")


if __name__ == "__main__":
    main()

