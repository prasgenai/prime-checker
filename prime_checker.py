import sys
import math


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def format_result(n: int) -> str:
    if is_prime(n):
        return f"{n} is a prime integer"
    return f"{n} is NOT a prime integer"


def interactive_mode():
    while True:
        user_input = input("Enter an integer (or quit/q/exit to stop): ").strip()
        if user_input.lower() in ("quit", "q", "exit"):
            print("Goodbye!")
            return
        try:
            n = int(user_input)
        except ValueError:
            print(f"Error: '{user_input}' is not a valid integer. Try again.")
            continue
        print(format_result(n))


def main():
    if len(sys.argv) == 1:
        interactive_mode()
        return
    if len(sys.argv) != 2:
        print("Usage: prime_checker.py <integer>", file=sys.stderr)
        sys.exit(1)
    try:
        n = int(sys.argv[1])
    except ValueError:
        print(f"Error: '{sys.argv[1]}' is not a valid integer", file=sys.stderr)
        sys.exit(1)
    print(format_result(n))


if __name__ == "__main__":
    main()
