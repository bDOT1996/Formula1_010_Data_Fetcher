FROM python:3.10-slim

# Ustawienie katalogu roboczego
WORKDIR /app

# Dodanie pliku z zależnościami i ich instalacja
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie kodu źródłowego (logika fetchera)
#COPY f1_data_fetcher/ ./f1_data_fetcher/
#COPY fetcher.py .

COPY utils/ ./utils/
COPY run.py .
COPY .env .
COPY input/ ./input/

# Ustawienie logów - mają wyświetlać się natychmiast, nie po zakończeniu procesów
ENV PYTHONUNBUFFERED=1

# Domyślny punkt wejścia — można nadpisać przez CMD
#ENTRYPOINT ["python", "-u", "fetcher.py"]
ENTRYPOINT ["python", "run.py"]
