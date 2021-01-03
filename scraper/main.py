from scraper import scraper_classes as SC

if __name__ == "__main__":
    scraper = SC.GoogleScraper()
    scraper.scrape_dates_links()
    scraper.scrape_articles()