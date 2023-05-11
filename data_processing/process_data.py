import os
import re
import uuid
from datetime import datetime

import config
import numpy as np
import pandas as pd
import utils
from tqdm import tqdm


class ProcessData:
    def __init__(self, folder_path: str) -> None:
        """
        Initializes the ProcessData class to create facts and dimension tables from the raw JSON files.
        :param folder_path: path to the data folder
        """
        self.folder_path = folder_path
        self.files = []

        # define fact tables
        self.fact_accident = pd.DataFrame(columns=config.fact_table_columns)

        # define dimension tables as per the data model design
        self.dim_date = pd.DataFrame(columns=config.dim_date_columns)
        self.dim_time = pd.DataFrame(columns=config.dim_time_columns)
        self.dim_airline = pd.DataFrame(columns=config.dim_airline_columns)
        self.dim_route = pd.DataFrame(columns=config.dim_route_columns)
        self.dim_aircraft_type = pd.DataFrame(
            columns=config.dim_aircraft_type_columns
        )

    def read_files(self) -> None:
        """
        Reads the files from the data folder.
        """
        self.files = os.listdir(self.folder_path)

    def update_tables(
        self,
        fact_accident_temp,
        dim_date_temp,
        dim_time_temp,
        dim_airline_temp,
        dim_route_temp,
        dim_aircraft_type_temp,
    ):
        """
        Updates the global fact and dimension tables with the data from one file.
        :param fact_accident_temp: fact table from one file
        :param dim_date_temp: date dimension table from one file
        :param dim_time_temp: time dimension table from one file
        :param dim_airline_temp: airline dimension table from one file
        :param dim_route_temp: route dimension table from one file
        :param dim_aircraft_type_temp: aircraft_type dimension table from one file
        """

        # concatenate fact tables
        self.fact_accident = pd.concat(
            [self.fact_accident, fact_accident_temp], axis=0
        )

        # concatenate dimension tables
        self.dim_date = pd.concat([self.dim_date, dim_date_temp], axis=0)
        self.dim_time = pd.concat([self.dim_time, dim_time_temp], axis=0)
        self.dim_airline = pd.concat(
            [self.dim_airline, dim_airline_temp], axis=0
        )
        self.dim_route = pd.concat([self.dim_route, dim_route_temp], axis=0)
        self.dim_aircraft_type = pd.concat(
            [self.dim_aircraft_type, dim_aircraft_type_temp], axis=0
        )

        # reset indexes of all the dataframes
        self.fact_accident.reset_index(drop=True, inplace=True)
        self.dim_date.reset_index(drop=True, inplace=True)
        self.dim_time.reset_index(drop=True, inplace=True)
        self.dim_airline.reset_index(drop=True, inplace=True)
        self.dim_route.reset_index(drop=True, inplace=True)
        self.dim_aircraft_type.reset_index(drop=True, inplace=True)

    def process_files_util(self, data: pd.DataFrame) -> None:
        """
        Creates fact and dimension tables from one file and adds it to the global tables.
        :param data: raw dataframe from one file
        """

        # define temporary tables
        fact_accident_temp = pd.DataFrame(columns=config.fact_table_columns)
        dim_date_temp = pd.DataFrame(columns=config.dim_date_columns)
        dim_time_temp = pd.DataFrame(columns=config.dim_time_columns)
        dim_airline_temp = pd.DataFrame(columns=config.dim_airline_columns)
        dim_route_temp = pd.DataFrame(columns=config.dim_route_columns)
        dim_aircraft_type_temp = pd.DataFrame(
            columns=config.dim_aircraft_type_columns
        )

        """
        For each row of the data, populate the fact and the dimension tables along with generating surrogate keys
        for each of them.
        """
        for idx, row in data.iterrows():
            fact_row = []
            dim_date_row = []
            dim_time_row = []
            dim_airline_row = []
            dim_route_row = []
            dim_aircraft_type_row = []

            # fact surrogate key
            fact_id = uuid.uuid4().__str__()
            fact_row.append(fact_id)

            # date dimension
            date_id = uuid.uuid4().__str__()
            date = datetime.strptime(row["date"], config.date_format)
            day = date.day
            month = date.month
            year = date.year
            day_of_week = date.strftime("%A")
            dim_date_row.extend([date_id, day, month, year, day_of_week])
            fact_row.append(date_id)

            # time dimension
            if str(row["time"]).strip() != "?":
                time_id = uuid.uuid4().__str__()
                tmp = str(row["time"])
                if len(str(row["time"])) < 4:
                    tmp = "0" + tmp
                time_match = re.search(config.time_format, tmp)
                if time_match:
                    time_str = time_match.group(0)
                    hours, minutes = int(str(time_str)[:2]), int(
                        str(time_str)[2:]
                    )
                    dim_time_row.extend([time_id, hours, minutes])
                    fact_row.append(time_id)
                else:
                    fact_row.append(None)
            else:
                fact_row.append(None)

            # airline dimension
            if row["airline_operator"].strip() != "?":
                airline_id = uuid.uuid4().__str__()
                dim_airline_row.extend(
                    [
                        airline_id,
                        utils.validate_missing(row["airline_operator"]),
                    ]
                )
                fact_row.append(airline_id)
            else:
                fact_row.append(None)

            # routes dimension
            if row["route"].strip() != "?":
                route_id = uuid.uuid4().__str__()
                if "-" in row["route"]:
                    source = row["route"].split("-")[0].strip()
                    destination = row["route"].split("-")[0].strip()
                    dim_route_row.extend([route_id, None, source, destination])
                else:
                    dim_route_row.extend(
                        [route_id, row["route"].strip(), None, None]
                    )

                fact_row.append(route_id)
            else:
                fact_row.append(None)

            # aircraft type dimension
            if row["aircraft_type"].strip() != "?":
                aircraft_type_id = uuid.uuid4().__str__()
                dim_aircraft_type_row.extend(
                    [aircraft_type_id, row["aircraft_type"]]
                )
                fact_row.append(aircraft_type_id)
            else:
                fact_row.append(None)

            # fact table values
            fact_row.append(utils.validate_missing(row["location"]))
            fact_row.append(utils.validate_missing(row["flight_no"]))
            fact_row.append(utils.validate_missing(row["icao_reg"]))
            fact_row.append(utils.validate_missing(row["cn_ln"]))

            (
                total_aboard,
                passengers_aboard,
                crew_aboard,
            ) = utils.get_count_details(row["aboard"])
            fact_row.extend([total_aboard, passengers_aboard, crew_aboard])

            (
                total_fatalities,
                passengers_fatalities,
                crew_fatalities,
            ) = utils.get_count_details(row["fatalities"])
            fact_row.extend(
                [total_fatalities, passengers_fatalities, crew_fatalities]
            )

            ground_fatalities = (
                int(str(row["ground"]).strip())
                if str(row["ground"]).strip() != "?"
                else np.nan
            )
            fact_row.append(ground_fatalities)

            summary = (
                row["summary"].strip()
                if row["summary"].strip() != "?"
                else np.nan
            )
            fact_row.append(summary)

            fact_accident_temp.loc[len(fact_accident_temp)] = fact_row

            if len(dim_date_row) > 0:
                dim_date_temp.loc[len(dim_date_temp)] = dim_date_row
            if len(dim_time_row) > 0:
                dim_time_temp.loc[len(dim_time_temp)] = dim_time_row
            if len(dim_airline_row) > 0:
                dim_airline_temp.loc[len(dim_airline_temp)] = dim_airline_row
            if len(dim_route_row) > 0:
                dim_route_temp.loc[len(dim_route_temp)] = dim_route_row
            if len(dim_aircraft_type_row) > 0:
                dim_aircraft_type_temp.loc[
                    len(dim_aircraft_type_temp)
                ] = dim_aircraft_type_row

        # add data to the global tables
        self.update_tables(
            fact_accident_temp,
            dim_date_temp,
            dim_time_temp,
            dim_airline_temp,
            dim_route_temp,
            dim_aircraft_type_temp,
        )

    def process_files(self) -> None:
        """
        Processes all the files one by one.
        """

        self.read_files()

        for file in tqdm(self.files):
            file_path = os.path.join(self.folder_path, file).replace("\\", "/")
            data = pd.read_json(file_path)
            data.columns = config.file_columns
            self.process_files_util(data)

        self.write_tables_to_parquet()

    def write_tables_to_parquet(self) -> None:
        """
        Write all the fact and dimension tables to parquet files.
        """
        # create the folder if not exists
        os.makedirs(config.output_folder_path, exist_ok=True)

        # writes the tables to files
        self.fact_accident.to_parquet(config.fact_accident_path)
        self.dim_date.to_parquet(config.dim_date_path)
        self.dim_time.to_parquet(config.dim_time_path)
        self.dim_airline.to_parquet(config.dim_airline_path)
        self.dim_route.to_parquet(config.dim_route_path)
        self.dim_aircraft_type.to_parquet(config.dim_aircraft_type_path)
