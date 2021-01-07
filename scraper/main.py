from scraper import scraper_classes as SC
from analysis.main import process_text
import time


def run_scraping():
    while True:
        scraper = SC.GoogleScraper()
        scraper.scrape_dates_links()
        scraper.scrape_articles()
        time.sleep(3)

def run_prediction():
    while True:
        process_text()
        time.sleep(3)



# if __name__ == "__main__":
#     run_scraping_and_prediction()