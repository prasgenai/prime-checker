# Prime Checker

A command-line tool that checks whether an integer is prime. Accepts numeric input or English words (e.g. "seventeen", "minus five").

## Features

- Numeric input: `python3 prime_checker.py 17`
- Word input: `python3 prime_checker.py "thirty one"`
- Interactive mode: run without arguments to enter a prompt loop
- Supports negative numbers and zero

## Usage

### CLI mode
```bash
python3 prime_checker.py 17        # 17 is a prime integer
python3 prime_checker.py 20        # 20 is NOT a prime integer
python3 prime_checker.py "three"   # three is a prime integer
```

### Interactive mode
```bash
python3 prime_checker.py
# Enter an integer (or quit/q/exit to stop): 13
# 13 is a prime integer
```

## Running with Docker

```bash
docker-compose run --rm app python3 prime_checker.py 17
```

## Running Tests

```bash
pip3 install -r requirements.txt
python3 -m pytest test_prime_checker.py -v
```

## Requirements

- Python 3.10+
- `word2number`
- `pytest` (for tests)
