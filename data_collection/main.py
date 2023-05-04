from configparser import ConfigParser

from web_scraper import WebScraper

if __name__ == "__main__":
    """
    Calls the web scraper and starts the scraping process.
    """
    # get configs
    config = ConfigParser()
    config.read("config.ini")
    web_url = config.get("web", "url")
    top_domain = config.get("web", "top_domain")
    print(f"Web URL: {web_url}")

    # scrape data
    scraper = WebScraper(web_url, top_domain)
    scraper.scrape()
