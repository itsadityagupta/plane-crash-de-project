import os
from configparser import ConfigParser

config = ConfigParser()
config.read(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
)

folder_path = config.get("files", "folder_path")
file_columns = config.get("files", "file_columns").split(",")

fact_table_columns = config.get("data-model", "fact_table_columns").split(",")
dim_date_columns = config.get("data-model", "dim_date_columns").split(",")
dim_time_columns = config.get("data-model", "dim_time_columns").split(",")
dim_airline_columns = config.get("data-model", "dim_airline_columns").split(
    ","
)
dim_route_columns = config.get("data-model", "dim_route_columns").split(",")
dim_aircraft_type_columns = config.get(
    "data-model", "dim_aircraft_type_columns"
).split(",")

date_format = "%B %d, %Y"
total_format = r"(\d+)"
time_format = r"\d{4}"
passenger_format = r"passengers:\s*(\d+)"
crew_format = r"crew:\s*(\d+)"

output_folder_path = config.get("output", "folder_path")

fact_accident_path = os.path.join(
    output_folder_path, "fact_accident.parquet"
).replace("\\", "/")
dim_date_path = os.path.join(output_folder_path, "dim_date.parquet").replace(
    "\\", "/"
)
dim_time_path = os.path.join(output_folder_path, "dim_time.parquet").replace(
    "\\", "/"
)
dim_airline_path = os.path.join(
    output_folder_path, "dim_airline.parquet"
).replace("\\", "/")
dim_route_path = os.path.join(output_folder_path, "dim_route.parquet").replace(
    "\\", "/"
)
dim_aircraft_type_path = os.path.join(
    output_folder_path, "dim_aircraft_type.parquet"
).replace("\\", "/")
