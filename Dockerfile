# Start from official Airflow image
FROM apache/airflow:2.8.1

# Install Linux packages needed for ODBC
USER root
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    apt-transport-https \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Switch to airflow user BEFORE pip install
USER airflow

# Install Python packages needed
RUN pip install pyodbc pandas snowflake-connector-python
