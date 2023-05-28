#!/bin/bash

# Function to handle script termination
cleanup() {
  # Delete the downloaded Apache Airflow .whl file
  rm -f apache-airflow.whl
}

# Register signal handler for script termination
trap cleanup EXIT

# Step 1: Download the Apache Airflow .whl file
curl -o apache-airflow.whl https://dlcdn.apache.org/airflow/2.6.1/apache_airflow-2.6.1-py3-none-any.whl

# Step 2: Install the downloaded Apache Airflow .whl file
pip install apache-airflow.whl

# Step 3: Install Python packages from requirements.txt without cache
pip install --no-cache-dir -r requirements-local.txt
