# Funkcja do buforowania i zapisu danych
import logging
import pandas as pd

from time import sleep

from class_APIClient import APIClient
from utils_load_parameters import get_snowflake_connection, get_parameters
from utils_write_to_snowflake import write_to_snowflake

# Inicjalizacja loggera
logger = logging.getLogger(__name__)

def fetch_and_buffer_data(
    param_file_path,
    api_url: str,
    buffer_size=1000
):
    """
    Iterates over API parameters, fetches data, buffers it in a DataFrame,
    and writes to Snowflake in chunks.
    """

    parameters = get_parameters(input_path = param_file_path)
    method = parameters["method"]
    param_list = parameters["params"]
    table_name = f"BRONZE_{method.upper()}"
    total = len(param_list)
   
    snowflake_conn_params = get_snowflake_connection()
    client = APIClient(api_url = api_url)

    buffer = pd.DataFrame()
    file_idx = 1

    logger.info(f"Starting API fetch for method '{method}'. Total requests: {total}")

    for idx, param_entry in enumerate(param_list, start=1):
        logger.info(f"[{idx}/{total}] Fetching data with parameters: {param_entry}")
        
        # Pobranie danych za pomocą metody fetch_data z APIClient
        df = client.fetch_data(endpoint=method, params=param_entry)
        
        # Sprawdzenie, czy dane zostały zwrócone i nie są puste
        if df is not None and not df.empty:
            buffer = pd.concat([buffer, df], ignore_index=True)
            logger.info(f"Buffered {len(df)} rows. Current buffer size: {len(buffer)}")

            if len(buffer) >= buffer_size:
                logger.info(f"Buffer reached {buffer_size} rows. Writing to Snowflake...")
                write_to_snowflake(
                    df = buffer.iloc[:buffer_size],
                    conn_params = snowflake_conn_params,
                    table_name = table_name
                )
                logger.info(f"Chunk {file_idx} written to Snowflake ({buffer_size} rows).")
                buffer = buffer.iloc[buffer_size:].reset_index(drop=True)
                file_idx += 1
        else:
            logger.warning(f"[{idx}/{total}] No data returned for parameters: {param_entry}")
        
        sleep(2)

    # Zapis pozostałych danych w buforze, jeśli nie jest pusty
    if not buffer.empty:
        logger.info(f"Writing remaining {len(buffer)} rows from buffer to Snowflake...")
        write_to_snowflake(
                df = buffer,
                conn_params = snowflake_conn_params,
                table_name = table_name
            )
        logger.info(f"Final {len(buffer)} rows written to Snowflake.")
    else:
        logger.info("No remaining data in buffer to write.")

    logger.info("API fetch and write process completed.")

        