import requests


def get_html(url: str) -> str:
    """
    Sends a GET request to the given URL to fetch the page content.
    :param url: website to scrape
    :return: Website HTML as string
    """
    response = requests.get(url)
    return response.text
