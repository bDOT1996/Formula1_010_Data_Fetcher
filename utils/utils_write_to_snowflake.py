import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import logging

# Inicjalizacja loggera
logger = logging.getLogger(__name__)


def write_to_snowflake(df, conn_params, table_name):
    """
    Writes a DataFrame to a Snowflake table.
    Args:
        df: pandas.DataFrame with data
        conn_params: dict with Snowflake connection parameters
        table_name: str - target table name in Snowflake
    Returns:
        bool: True if write succeeded, False otherwise
    """
    logger.info(f"[Snowflake] Starting write to table: {table_name} (rows: {len(df)})")

    try:
        conn = snowflake.connector.connect(**conn_params)

        success, nchunks, nrows, _ = write_pandas(
            conn=conn,
            df=df,
            table_name=table_name,
            auto_create_table=True,
            use_logical_type=True
        )

        if success:
            logger.info(f"[Snowflake] ✅ Successfully loaded {nrows} rows in {nchunks} chunks into table {table_name}")
        else:
            logger.warning(f"[Snowflake] ⚠️ Write operation failed for table {table_name}")

        return success

    except Exception as e:
        logger.error(f"[Snowflake] ❌ Error while writing to table {table_name}: {e}")
        return False

    finally:
        try:
            conn.close()
            logger.info(f"[Snowflake] Connection closed successfully")
        except Exception as e:
            logger.warning(f"[Snowflake] Warning when closing connection: {e}")
