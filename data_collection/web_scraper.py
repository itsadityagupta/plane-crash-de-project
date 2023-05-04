import json
from collections import defaultdict
from urllib.parse import urljoin

import utils
from bs4 import BeautifulSoup
from exceptions.table_exception import InsufficientTableException


class WebScraper:
    def __init__(self, url: str, top_domain: str) -> None:
        """
        Initializes a WebScraper object to start scraping from the given URL
        :param url: Website to scrape
        :param top_domain: Host name
        """
        self.url = url
        self.top_domain = top_domain

    def get_accident_url(self, year, suffix):
        """
        Creates a complete URL path.
        :param year: year of the accident
        :param suffix: path suffix of the accident
        :return: A complete URL path of the accident page
        """
        return urljoin(self.top_domain, str(year) + "/" + suffix)

    def scrape_accident(self, url) -> list:
        """
        Scrapes the accident details.
        :param url: A complete URL of the accident
        :return: list of accident details
        """
        print(f"Scraping accident url {url}")

        soup = BeautifulSoup(utils.get_html(url), "html.parser")
        rows = soup.find_all("tr")[1:]  # skip the header

        accident_details = []

        for row in rows:
            value = row.find_all("td")[1].string
            accident_details.append(value)

        return accident_details

    def write_year_data(self, year, data) -> None:
        """
        Writes the given data into a file.
        :param year: year of accidents
        :param data: accident details
        """
        year_data = defaultdict(list)

        for accident in data:
            year_data["year"].append(year)
            year_data["col1"].append(accident[0])
            year_data["col2"].append(accident[1])
            year_data["col3"].append(accident[2])
            year_data["col4"].append(accident[3])
            year_data["col5"].append(accident[4])
            year_data["col6"].append(accident[5])
            year_data["col7"].append(accident[6])
            year_data["col8"].append(accident[7])
            year_data["col9"].append(accident[8])
            year_data["col10"].append(accident[9])
            year_data["col11"].append(accident[10])
            year_data["col12"].append(accident[11])
            year_data["col13"].append(accident[12])

        with open(f"data_{year}.json", "w") as f:
            json.dump(year_data, f)

    def scrape_year(self, year, url) -> None:
        """
        Scrapes data for a year.
        :param year: year of the accident
        :param url: complete URL to the page of the year
        """
        print(f"Scraping year {year} and url {url}")

        soup = BeautifulSoup(utils.get_html(url), "html.parser")
        rows = soup.find_all("tr")[1:]  # skip the header
        year_data = []

        for row in rows:
            suffix = row.find_all("a")[0]["href"]
            accident_url = self.get_accident_url(year, suffix)
            year_data.append(self.scrape_accident(accident_url))

        self.write_year_data(year, year_data)

    def scrape(self) -> None:
        """
        Performs all the scraping.
        """
        soup = BeautifulSoup(utils.get_html(self.url), "html.parser")
        tables = soup.find_all("table")
        print(soup.contents)

        if len(tables) < 2:
            raise InsufficientTableException(
                f"Less than 2 tables found in the url: {self.url}"
            )
        else:
            second_table = tables[1].find_all("a")
            links = [
                urljoin(self.top_domain, link["href"]) for link in second_table
            ]
            years = [int(link.text.strip()) for link in second_table]

            for year, url in zip(years, links):
                self.scrape_year(year, url)
