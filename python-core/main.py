def analyze_numbers(numbers):
    result = {
        "count": 0,
        "sum": 0
    }

    for number in numbers:
        result["count"] += 1
        result["sum"] += number

    return result


print(analyze_numbers([2, 4, 6, 8]))