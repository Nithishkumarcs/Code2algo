def factorial(n):
    """Calculates factorial recursively."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

if __name__ == "__main__":
    num = 5
    result = factorial(num)
    print(f"Factorial of {num} is {result}")
