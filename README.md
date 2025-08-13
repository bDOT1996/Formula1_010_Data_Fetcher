# Formula1_010_Data_Fetcher

## Overview
This repository contains a Python-based application that processes data using parameters defined in `input/params.json`. The main script, `run.py`, is executed via Apache Airflow. The project leverages Docker for containerization and includes utilities for API interactions, data buffering, logging, and writing to Snowflake.

## Prerequisites
- **Docker** and **Docker Compose** for containerized execution
- **Python 3.8+** for local development
- **Snowflake account** with a configured warehouse, database, and schema
- Access to the [OpenF1 API](https://openf1.org/) (no authentication required)
- **Apache Airflow** (for future orchestration of `run.py`)

## Installation and Configuration
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```
2. **Environment Variables**: Create `.env` with Snowflake credentials:
   ``` plaintext
   SF_ACCOUNT=your_snowflake_ACCOUNT
   SF_USER=your_snowflake_USER
   SF_PASSWORD=your_snowflake_PASSWORD
   SF_DATABASE=your_snowflake_DATABASE
   SF_SCHEMA=your_snowflake_SCHEMA
   SF_WAREHOUSE=your_snowflake_WAREHOUSE
   ```
3. **Parameters**: Define OpenF1 API parameters in `input/params.json`. Example:
   ```json
   {
      "method": "car_data",
      "params": [
         { "MEETING_KEY": 1141, "session_key": 7953, "driver_number": 31, "date_start": "2023-03-05 15:00:00.000", "date_end": "2023-03-05 17:00:00.000" }
      ]
   }
   ```
4. **Snowflake**: Ensure a warehouse, database, and schema are created in Snowflake. The pipeline will handle table creation automatically.
5. Build and run the Docker container - it automatically runs:
   ```bash
   docker-compose up --build
   ```

## Project Structure
```
.
├── docker-compose.yml                    # Docker Compose configuration
├── Dockerfile                            # Docker image definition
├── .env                                  # Environment variables
├── .gitignore                            # Git ignore file
├── images/
│   └── ERP_diagram.pdf                   # ERD diagram for the database
├── input/
│   └── params.json                       # Input parameters for run.py
├── README_filters.md                     # Additional documentation (filters)
├── README.md                             # This file
├── requirements.txt                      # Python dependencies
├── run.py                                # Main script executed by Airflow
└── utils/
    ├── class_APIClient.py                # API client class
    ├── class_APIRequestBuilder.py        # API request builder class
    ├── __init__.py                       # Python package initialization
    ├── utils_fetch_and_buffer_data.py    # Data fetching and buffering utilities
    ├── utils_load_parameters.py          # Parameter loading utilities
    ├── utils_loging_setup.py             # Logging configuration
    └── utils_write_to_snowflake.py       # Snowflake writing utilities
```


## Future Plans (in other repos Formula1_*)
- Deploy the pipeline to a cloud environment.
- Integrate with Airflow for automated DAG execution.
- Add DBT for data transformation and modeling.
- Incorporate Grafana for data visualization and monitoring.
- Use Terraform for infrastructure provisioning.

## References
- [OpenF1 API Documentation](https://openf1.org)


