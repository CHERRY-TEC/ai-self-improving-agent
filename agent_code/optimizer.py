import math


def calculate_stats(numbers: list[float]) -> dict:
    """Calculate basic statistics for a list of numbers."""
    if not numbers:
        return {"error": "Empty list"}
    
    n = len(numbers)
    mean = sum(numbers) / n
    variance = sum((x - mean) ** 2 for x in numbers) / n
    std_dev = math.sqrt(variance)
    sorted_nums = sorted(numbers)
    median = sorted_nums[n // 2] if n % 2 else (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2
    
    return {
        "count": n,
        "mean": mean,
        "median": median,
        "std_dev": std_dev,
        "min": min(numbers),
        "max": max(numbers),
        "range": max(numbers) - min(numbers),
    }


def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def fibonacci(n: int) -> list[int]:
    """Generate fibonacci sequence up to n terms."""
    if n <= 0:
        return []
    if n == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, n):
        seq.append(seq[-1] + seq[-2])
    return seq


def binary_search(arr: list[int], target: int) -> int:
    """Perform binary search on sorted array."""
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


if __name__ == "__main__":
    print("Testing agent code...")
    print(calculate_stats([1, 2, 3, 4, 5]))
    print(f"Is 17 prime? {is_prime(17)}")
    print(f"First 10 Fibonacci: {fibonacci(10)}")
    print(f"Search for 5 in [1,2,3,4,5]: {binary_search([1,2,3,4,5], 5)}")