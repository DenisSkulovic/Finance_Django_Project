from scraper import scraper_classes as SC
from analysis.main import process_text


def run_scraping_and_prediction():
    scraper = SC.GoogleScraper()
    scraper.scrape_dates_links()
    scraper.scrape_articles()
    process_text()

if __name__ == "__main__":
    run_scraping_and_prediction()