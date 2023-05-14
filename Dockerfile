FROM apache/airflow:2.6.0
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
ENV PYTHONPATH "${PYTHONPATH}:/opt/airflow/data_processing"