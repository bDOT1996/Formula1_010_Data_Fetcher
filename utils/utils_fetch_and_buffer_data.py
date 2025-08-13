# Funkcja do buforowania i zapisu danych
import logging
import pandas as pd

from datetime import datetime, timedelta
from time import sleep

from .class_APIClient import APIClient
from .utils_load_parameters import get_snowflake_connection, get_parameters
from .utils_write_to_snowflake import write_to_snowflake

# Inicjalizacja loggera
logger = logging.getLogger(__name__)

def fetch_and_buffer_data(
    param_file_path,
    api_url: str,
    buffer_size=5000
):
    """
    Fetches data from API using parameters, buffers it in a DataFrame, and writes to Snowflake in chunks.
    Splits date range into 15-second intervals if date_start and date_end are provided.

    Args:
        param_file_path (str): Path to the parameter file.
        api_url (str): API URL for data fetching.
        buffer_size (int, optional): Number of rows to buffer before writing to Snowflake. Defaults to 1000.
    """
    
    # Load parameters and initialize connections
    parameters = get_parameters(input_path=param_file_path)
    method = parameters["method"]
    param_list = parameters["params"]
    table_name = f"BRONZE_{method.upper()}"
    total_params = len(param_list)

    snowflake_conn_params = get_snowflake_connection()
    client = APIClient(api_url=api_url)
    buffer = pd.DataFrame()
    file_idx = 1

    if method == "intervals":
        delta_time = 60
    elif method in {"car_data", "location"}:
        delta_time = 15
    else:
        delta_time = 360


    logger.info(f"Starting API fetch for method '{method}'. Total requests: {total_params}")

    def generate_sub_requests(param_entry: dict, delta_time: int) -> list:
        """
        Generate sub-requests for date range with delta_time intervals.
        """
        if 'date_start' not in param_entry or 'date_end' not in param_entry:
            return [param_entry]
        
        try:
            start = datetime.fromisoformat(param_entry['date_start'])
            end = datetime.fromisoformat(param_entry['date_end'])
            delta = timedelta(seconds=delta_time)
            sub_requests = []

            current = start
            while current < end:
                next_end = min(current + delta, end)
                sub_params = param_entry.copy()
                sub_params['date_start'] = current.isoformat()
                sub_params['date_end'] = next_end.isoformat()
                sub_requests.append(sub_params)
                current = next_end
            return sub_requests or [param_entry]  # Fallback if no sub-requests
        except ValueError as e:
            logger.error(f"Error parsing dates in param_entry: {param_entry}. Error: {e}")
            return [param_entry]

    def write_buffer_if_full() -> None:
        """
        Write buffer to Snowflake if it reaches the buffer size and reset buffer.
        # is memory size 
        """
        nonlocal buffer, file_idx
        #buffer_memory_size = buffer.memory_usage(deep=True).sum() / (1024 * 1024) # Mb
        if len(buffer) >= buffer_size:
            print(df)
            logger.info(f"Buffer reached {buffer_size} rows. Writing to Snowflake...")
            write_to_snowflake(
                df = buffer.iloc[:buffer_size],
                #df = buffer,
                conn_params = snowflake_conn_params,
                table_name = table_name
            )
            logger.info(f"Chunk {file_idx} written to Snowflake ({buffer_size} rows).")
            buffer = buffer.iloc[buffer_size:].reset_index(drop=True)
            #buffer = buffer.iloc[0:0].reset_index(drop=True)  
            file_idx += 1
            
        

    for idx, param_entry in enumerate(param_list, start=1):
        logger.info(f"[{idx}/{total_params}] Processing parameter entry: {param_entry}")
        sub_requests = generate_sub_requests(param_entry=param_entry, delta_time=delta_time)
        sub_total = len(sub_requests)

        if sub_total > 1:
            logger.info(f"[{idx}/{total_params}] Splitting into {sub_total} sub-requests.")

        for sub_idx, sub_params in enumerate(sub_requests, 1):
            log_prefix = f"[{idx}/{total_params}]" + (f" [{sub_idx}/{sub_total}]" if sub_total > 1 else "")
            logger.info(f"{log_prefix} Fetching data with parameters: {sub_params}")

            df = client.fetch_data(endpoint=method, params=sub_params)
            if df is not None and not df.empty:
                buffer = pd.concat([buffer, df], ignore_index=True)
                logger.info(f"Buffered {len(df)} rows. Current buffer size: {len(buffer)}")
                write_buffer_if_full()
            else:
                logger.warning(f"{log_prefix} No data returned for parameters: {sub_params}")

            sleep(2)

    # Write remaining buffer data
    if not buffer.empty:
        logger.info(f"Writing remaining {len(buffer)} rows to Snowflake...")
        write_to_snowflake(df=buffer, conn_params=snowflake_conn_params, table_name=table_name)
        logger.info(f"Final {len(buffer)} rows written to Snowflake.")
    else:
        logger.info("No remaining data in buffer to write.")

    logger.info("API fetch and write process completed.")
        