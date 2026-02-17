import sys
import math

from word2number import w2n


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def parse_input(text: str) -> tuple:
    text = text.strip()
    try:
        n = int(text)
        return (n, str(n))
    except ValueError:
        pass
    try:
        lower = text.lower()
        if lower.startswith("minus "):
            n = -w2n.word_to_num(lower[6:])
        elif lower.startswith("negative "):
            n = -w2n.word_to_num(lower[9:])
        else:
            n = w2n.word_to_num(text)
        return (n, text)
    except ValueError:
        raise ValueError(f"Invalid input: '{text}'")


def format_result(n: int, label: str = None) -> str:
    display = label if label is not None else str(n)
    if is_prime(n):
        return f"{display} is a prime integer"
    return f"{display} is NOT a prime integer"


def interactive_mode():
    while True:
        user_input = input("Enter an integer (or quit/q/exit to stop): ").strip()
        if user_input.lower() in ("quit", "q", "exit"):
            print("Goodbye!")
            return
        try:
            n, label = parse_input(user_input)
        except ValueError:
            print(f"Error: '{user_input}' is not a valid input. Try again.")
            continue
        print(format_result(n, label))


def main():
    if len(sys.argv) == 1:
        interactive_mode()
        return
    if len(sys.argv) != 2:
        print("Usage: prime_checker.py <integer>", file=sys.stderr)
        sys.exit(1)
    try:
        n, label = parse_input(sys.argv[1])
    except ValueError:
        print(f"Error: '{sys.argv[1]}' is not a valid input", file=sys.stderr)
        sys.exit(1)
    print(format_result(n, label))


if __name__ == "__main__":
    main()
