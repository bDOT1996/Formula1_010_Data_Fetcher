#from utils_fetch_and_buffer_data import fetch_and_buffer_data
from utils.utils_fetch_and_buffer_data_copy import fetch_and_buffer_data
from utils.utils_loging_setup import setup_logging
import logging
import os

# Pobierz tryb logowania z zmiennej środowiskowej, domyślnie "console"
log_mode = os.getenv("LOG_MODE", "console")

# Konfiguracja logowania
setup_logging(log_mode=log_mode)

# Inicjalizacja loggera
logger = logging.getLogger(__name__)

def main():
    # Ścieżka do pliku params.json w kontenerze
    param_file_path = "./input/params.json"

    BASE_URL = "https://api.openf1.org/v1"
    # Rozmiar bufora (domyślnie 1000, można dostosować)
    buffer_size = 5000
    
    # Wywołanie funkcji
    fetch_and_buffer_data(
        param_file_path=param_file_path,
        api_url=BASE_URL,
        buffer_size=buffer_size
    )

if __name__ == "__main__":
    main()