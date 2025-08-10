import logging
import sys
import os

def setup_logging(log_mode="console"):
    """
    Configure logging based on the specified mode.
    - 'console': Logs to stdout (for testing in Docker).
    - 'file': Logs to a file (for production).
    - 'both': Logs to both stdout and file.
    """
    # Podstawowa konfiguracja loggera
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Poziom logowania

    # Usuń istniejące handlery, aby uniknąć duplikacji
    logger.handlers.clear()

    # Format logów
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Konfiguracja handlerów na podstawie trybu
    if log_mode == "console" or log_mode == "both":
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)
        # Wymuś flush dla natychmiastowego wyświetlania
        console_handler.flush = sys.stdout.flush

    if log_mode == "file" or log_mode == "both":
        file_handler = logging.FileHandler('app.log')
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

    # W przypadku nieprawidłowego trybu, domyślnie loguj do konsoli
    if log_mode not in ["console", "file", "both"]:
        logging.warning(f"Nieprawidłowy tryb logowania: {log_mode}. Ustawiam domyślnie 'console'.")
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)
        console_handler.flush = sys.stdout.flush