from scraper import scraper_classes as SC
from scraper import scraper_exceptions as SE
from pathlib import Path

if __name__ == '__main__':

    scraper = SC.GoogleScraper(
        keyword='Airline Stocks', 
        search_start_date='06/01/2019', 
        periods=int(365/2),
        save_to_location = Path.cwd(),
        word_count_threshold = 500, 
        periodicity='2D',
        google_results_pages=2,
        headless=False,
        )
    # scraper.scrape()