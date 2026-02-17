FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY prime_checker.py test_prime_checker.py ./

CMD ["python", "prime_checker.py"]
