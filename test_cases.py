"""
Test cases for the self-improving agent.
"""
import math

TEST_CASES = [
    # calculate_stats tests
    {
        "function": "calculate_stats",
        "args": ([1, 2, 3, 4, 5],),
        "expected": {
            "count": 5,
            "mean": 3.0,
            "median": 3,
            "std_dev": math.sqrt(2.0),
            "min": 1,
            "max": 5,
            "range": 4,
        }
    },
    {
        "function": "calculate_stats",
        "args": ([10],),
        "expected": {
            "count": 1,
            "mean": 10.0,
            "median": 10,
            "std_dev": 0.0,
            "min": 10,
            "max": 10,
            "range": 0,
        }
    },
    {
        "function": "calculate_stats",
        "args": ([],),
        "expected": {"error": "Empty list"}
    },
    
    # is_prime tests
    {"function": "is_prime", "args": (2,), "expected": True},
    {"function": "is_prime", "args": (17,), "expected": True},
    {"function": "is_prime", "args": (1,), "expected": False},
    {"function": "is_prime", "args": (4,), "expected": False},
    {"function": "is_prime", "args": (97,), "expected": True},
    
    # fibonacci tests
    {"function": "fibonacci", "args": (0,), "expected": []},
    {"function": "fibonacci", "args": (1,), "expected": [0]},
    {"function": "fibonacci", "args": (5,), "expected": [0, 1, 1, 2, 3]},
    {"function": "fibonacci", "args": (10,), "expected": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]},
    
    # binary_search tests
    {"function": "binary_search", "args": ([1, 2, 3, 4, 5], 3), "expected": 2},
    {"function": "binary_search", "args": ([1, 2, 3, 4, 5], 1), "expected": 0},
    {"function": "binary_search", "args": ([1, 2, 3, 4, 5], 6), "expected": -1},
]
