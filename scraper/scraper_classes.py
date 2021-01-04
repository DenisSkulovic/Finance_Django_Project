import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome, Remote
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
import os
from dateutil.relativedelta import relativedelta
import time
from typing import List
from abc import ABC, abstractproperty, abstractmethod
from pandas import to_datetime
from django.contrib.auth import get_user_model
from scraper import scraper_exceptions as SE
from scraper.models import Text, Article, Request, ProcessingStatus
User = get_user_model()





class BaseScraper:
    
    def __init__(self):
        self.browser = None
                        
    @SE.ExceptionHandler(SE.BrowserStartException, True)
    def _open_new_browser(self):
        options = ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2,
                "download.prompt_for_download": False,
                }
        options.add_experimental_option("prefs",prefs)
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--use-gl=desktop')
        options.add_argument('--log-level=3')
        options.add_argument("--disable-extensions")
        options.add_argument("--incognito")
        options.add_argument("--disable-download-notification")
        # options.add_argument("--headless")
        # options.add_argument("--disable-dev-shm-usage")
        # options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

        # browser = Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
        browser = Chrome(executable_path=ChromeDriverManager().install(), options=options)
        return browser
    
        
    @SE.ExceptionHandler(SE.BrowseToPageException, raise_error=True)
    def _browse_to_page(self, url):   
        self.browser.get(url)
        
    # The following methods were created to be used instead of the
    # original simple Selenium methods that search for elements immediately without
    # giving the browser time to finish loading the elements.
    
    # by xpath
    @SE.ExceptionHandler(SE.GetElementException, raise_error=True)    
    def _get_element_by_xpath(self, xpath, wait_sec=5):
        return (WebDriverWait(self.browser, wait_sec)
            .until(EC.presence_of_all_elements_located((By.XPATH, xpath)))[0])
    
    @SE.ExceptionHandler(SE.GetElementException, raise_error=True)    
    def _get_elements_by_xpath(self, xpath, wait_sec=5):
        return (WebDriverWait(self.browser, wait_sec)
            .until(EC.presence_of_all_elements_located((By.XPATH, xpath))))
    
    
    # by class name
    @SE.ExceptionHandler(SE.GetElementException, raise_error=True)        
    def _get_element_by_class_name(self, class_name, wait_sec=5):
        return (WebDriverWait(self.browser, wait_sec)
            .until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name)))[0])
    
    @SE.ExceptionHandler(SE.GetElementException, raise_error=True)                    
    def _get_elements_by_class_name(self, class_name, wait_sec=5):
        return (WebDriverWait(self.browser, wait_sec)
            .until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))))
       
       
    # by css selector
    @SE.ExceptionHandler(SE.GetElementException, raise_error=True)                              
    def _get_element_by_css_selector(self, css_selector, wait_sec=5):
        return (WebDriverWait(self.browser, wait_sec)
            .until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))[0])

    @SE.ExceptionHandler(SE.GetElementException, raise_error=True)                              
    def _get_elements_by_css_selector(self, css_selector, wait_sec=5):
        return (WebDriverWait(self.browser, wait_sec)
            .until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector))))


    # by tag name
    @SE.ExceptionHandler(SE.GetElementException, raise_error=True)                                  
    def _get_element_by_tag_name(self, tag_name, wait_sec=5):
        return (WebDriverWait(self.browser, wait_sec)
            .until(EC.presence_of_all_elements_located((By.TAG_NAME, tag_name)))[0])

    @SE.ExceptionHandler(SE.GetElementException, raise_error=True)                                  
    def _get_elements_by_tag_name(self, tag_name, wait_sec=5):
        return (WebDriverWait(self.browser, wait_sec)
            .until(EC.presence_of_all_elements_located((By.TAG_NAME, tag_name))))


    # by id
    @SE.ExceptionHandler(SE.GetElementException, raise_error=True)         
    def _get_element_by_id(self, id, wait_sec=5):
        return (WebDriverWait(self.browser, wait_sec)
            .until(EC.presence_of_all_elements_located((By.ID, id))))[0]   
    











class GoogleScraper(BaseScraper):
    
    def __init__(self, periods='', browser_wait_time = 5, word_count_threshold= 500, **kwargs):
        super().__init__(**kwargs)
        self.browser_wait_time = browser_wait_time
        self.word_count_threshold = word_count_threshold

    @SE.ExceptionHandler(SE.BrowserStartException, raise_error=True)
    def _change_google_to_english(self):
        lang_panel = self._get_element_by_id('SIvCob')
        lang_panel.find_element_by_xpath("//*[contains(text(), 'English')]").click()
          

    @SE.ExceptionHandler(SE.InfoCollectionException, raise_error=False)
    def _collect_p_h_tags(self):
        p_h_elements = self._get_elements_by_css_selector("p, h1, h2, h3, h4, h5, h6", self.browser_wait_time)
        results = []
        for elem in p_h_elements:
            if elem.text:
                results.append((elem.tag_name, elem.text, ))
        return results


    @SE.ExceptionHandler(SE.InfoCollectionException, raise_error=False)     
    def _collect_title(self):
        return (self._get_element_by_xpath('/html/head/title', self.browser_wait_time)
                    .get_attribute('textContent')
                    .strip())

    
    @staticmethod
    @SE.ExceptionHandler(SE.DateRangeGenerationException, raise_error=True)
    def generate_date_ranges(start_date, periods, periodicity):
        """Generate two lists with period start and end dates.

        Args:
            start_date (str): Google search period starting date string.
            periods (int): Number of periods to scrape. (e.g. scraping 10 periods, 3 days each will scrape data ranging 30 days)
            periodicity (str): Length of periods (e.g. '4D' will search periods spanning 4 days each)

        Raises:
            ValueError: 'periodicity' cannot be shorter than daily.

        Returns:
            tuple(list[datetime], list[datetime]): Tuple containing two lists of datetime objects. First contains the period start dates, the second one contains period end dates. Used in setting time periods in Google Search Tools.
        """
        print('periodicity: ', periodicity)
        if periodicity in ['BH','H','T','min','S','L','ms','us','U','N']:
            raise ValueError('Scraper does not support periodicities shorter than daily.')
        if periodicity in ['D','B']:
            print('recognized D')
            if periods==1:
                from_dates = [pd.to_datetime(start_date)]
                print('from_dates: ', from_dates)
                to_dates = [pd.to_datetime(start_date)]
                print('to_dates: ', to_dates)
                print('[(from_dates[0], to_dates[0])]: ', [(from_dates[0], to_dates[0])])
                return [(from_dates[0], to_dates[0])]
            from_dates = pd.date_range(start_date, periods=periods, freq=periodicity)
            to_dates = from_dates.copy()

        else:
            if periods==1:
                from_dates = pd.date_range(start_date, periods=2, freq=periodicity)
                to_dates = pd.date_range(from_dates[1]+relativedelta(days=-1), periods=2, freq=periodicity)
                return [(from_dates[0], to_dates[0])]
            else:
                from_dates = pd.date_range(start_date, periods=periods, freq=periodicity)
                to_dates = pd.date_range(from_dates[1]+relativedelta(days=-1), periods=periods, freq=periodicity)
                return list(zip(from_dates, to_dates))



    @SE.ExceptionHandler(SE.DateRangeGenerationException, raise_error=True)
    def _set_custom_date_period(self, from_date, to_date, current_period):
        """Set a custom search period in Google Search.

        Args:
            from_date (str): (format MM/DD/YYYY) Start of period.
            to_date (str): (format MM/DD/YYYY) End of period.
        """
        
        # Wait for appearance of "Tools" panel (it is clicked elsewhere during the first time page is opened; does not need to be clicked again during all subsequent scrapings)      
        time.sleep(0.5)
        xpath = '//div[@class="hdtb-mn-cont"]'
        self._get_element_by_xpath(xpath, self.browser_wait_time)
        
        # click "Time" button
        time.sleep(0.5)
        xpath = '//div[@class="mn-hd-txt"]'
        self._get_element_by_xpath(xpath, self.browser_wait_time).click() 
        
        # click "Custom Range" button
        time.sleep(0.5)
        xpath = '//span[@role="menuitem" and @jsaction="EEGHee" and @tabindex="-1"]'
        self._get_element_by_xpath(xpath, self.browser_wait_time).click()            
        
        # enter "from" date into search tools
        time.sleep(0.5)
        from_path = "//*[@id='OouJcb']"
        from_field = self._get_element_by_xpath(from_path, self.browser_wait_time)
        try: from_field.clear().send_keys(from_date)
        except: from_field.send_keys(from_date)
        
        # enter "to" date into search tools
        time.sleep(0.5)
        to_path = "//*[@id='rzG2be']"
        to_field = self._get_element_by_xpath(to_path, self.browser_wait_time)
        try: to_field.clear().send_keys(to_date)
        except: to_field.send_keys(to_date)
        
        # click "Go" button
        time.sleep(0.5)
        go_path = '//g-button[@class="Ru1Ao BwGU8e fE5Rge"]'
        self._get_element_by_xpath(go_path, self.browser_wait_time).click()


    @staticmethod
    @SE.ExceptionHandler(SE.DateLinkCollectionException, raise_error=False)
    def _collect_date_link_from_element(element):
        href = element.find_element_by_tag_name('a').get_attribute('href')
        date = (element.find_element_by_class_name("f")
                    .get_attribute('textContent')
                    .split('—')[0]
                    .strip())
        return href, date
        
        
    @SE.ExceptionHandler(SE.DateLinkCollectionException, raise_error=True)
    def _collect_dates_links(self):
        xpaths_to_try = ["//div[@id='rso']/div[@class='g']/div[@class='rc']", 
                         "//div[@class='hlcw0c']/div[@class='g']/div[@class='rc']", 
                         "//div[@class='g']/span/div[@class='rc']",
                         ] # google results page has differing structure from time to time
        for xpath in xpaths_to_try:
            try:
                page_results = self._get_elements_by_xpath(xpath)
                if page_results:
                    print('page_results: ', len(page_results))
                    break
            except: pass
        dates = []
        links = []
        for result in page_results:
            try:
                link, date = self._collect_date_link_from_element(result)
                links.append(link)
                dates.append(date)
            except: pass
        return dates, links



    @SE.ExceptionHandler(SE.ClickException, raise_error=True)
    def _next_google_results_page(self, page_no):
        self._get_element_by_xpath(f'//a[@aria-label="Page {page_no}"]').click()

    @staticmethod
    def truncate_text_data(text_data: tuple, word_count_threshold: int) -> list:
        spaces_count = 0
        texts_to_keep = []
        for text in text_data:
            for char in text[1]:
                if char == ' ':
                    spaces_count += 1
            texts_to_keep.append(text)
            if spaces_count >= word_count_threshold:
                return texts_to_keep
        return text_data



    def scrape_dates_links(self, work_time_sec=120):
        if Request.objects.filter(status='Unprocessed').first() == None:
            print('dates links scraper exited')
            return

        scraper_status = ProcessingStatus.objects.get_or_create(name='SCRAPER')[0]
        if scraper_status.status == 'FREE':
            try:

                scraper_status.status='BUSY'
                scraper_status.save()
                
                self.browser = self._open_new_browser()
                start = time.time()
                while True:
                    request = Request.objects.filter(status='Unprocessed').first()
                    
                    if request == None:
                        print('dates links scraper exited')
                        break
                    
                    self._browse_to_page('https://www.google.com/')
                    try:
                        self._change_google_to_english()
                    except:
                        pass
                    self._get_element_by_xpath('//input[@type="text"]').send_keys(request.keyword) #enter keyword
                    time.sleep(0.5)
                    self._get_element_by_xpath("//input[@type='submit']").click() #submit keyword for search

                    # loop through date periods
                    current_period = 1
                    date_ranges = self.generate_date_ranges(request.search_start_date, request.periods, request.periodicity)
                    for from_d, to_d in date_ranges:
                        from_d = from_d.strftime('%m/%d/%Y')
                        to_d = to_d.strftime('%m/%d/%Y')
                        # ensure the current results page is not larger than variable "google_results_pages"
                        current_page = 1
                        while current_page <= request.google_results_pages:
                            if current_page == 1:
                                if current_period == 1:
                                    xpath = '//div[@id="hdtb-tls"]'
                                    self._get_element_by_xpath(xpath).click() # clicking Tools button, stays active during subsequent results pages so no need to repeat step
                                self._set_custom_date_period(from_d, to_d, current_period)
                                dates, links = self._collect_dates_links()
                                for pair in zip(dates, links):
                                    try:
                                        date = to_datetime(pair[0])
                                        link = pair[1]
                                        request.article_set.create(date=date, link=link)
                                    except: print('failed to register link-date pair')
                                current_page += 1

                            elif current_page > 1:
                                try:
                                    self._next_google_results_page(str(current_page))
                                    dates, links = self._collect_dates_links()
                                    for pair in zip(dates, links):
                                        try:
                                            
                                            date = to_datetime(pair[0])
                                            link = pair[1]
                                            request.article_set.create(date=date, link=link)
                                        except: print('failed to register link-date pair')
                                    current_page += 1
                                except:
                                    current_page = request.google_results_pages+1
                        current_period +=1
                    request.status = 'Processing'
                    request.save()
                    if time.time() - start > work_time_sec:
                        break
            except:
                print('date_link scraper failed')
            finally:
                self.browser.quit()
                scraper_status.status='FREE'
                scraper_status.save()
        else:
            print('scraper is busy')

    
    def scrape_articles(self, work_time_sec=120):
        if Article.objects.filter(status='Unprocessed').first() == None:
            print('article scraper exited')
            return

        scraper_status = ProcessingStatus.objects.get_or_create(name='SCRAPER')[0]
        
        if scraper_status.status == 'FREE':
            try:

                scraper_status.status='BUSY'
                scraper_status.save()

                self.browser = self._open_new_browser()
                main_tab = self.browser.window_handles[0] # save the handle of the main search tab
                start = time.time()
                while True:

                    article = Article.objects.filter(status='Unprocessed').first()
                    
                    if article == None:
                        print('article scraper exited')
                        break

                    self.browser.execute_script(f"window.open('{article.link}', 'new window')") # open link in a new tab
                    self.browser.switch_to.window(window_name=self.browser.window_handles[1]) # switch Selenium to the new tab

                    title = self._collect_title()
                    results = self._collect_p_h_tags()

                    results = self.truncate_text_data(results, self.word_count_threshold)

                    for i, result in enumerate(results):

                        tag_name, text = result

                        article.text_set.create(text=text,
                                                tag=tag_name,
                                                position=i,
                                                )
                    article.title = title
                    article.status = 'Processing'
                    article.save()

                    try: # apparently google sometimes downloads a PDF and immediately closes the window, so try only tries to close if its already gone
                        self.browser.close() # close the article tab
                    except: pass
                    self.browser.switch_to.window(window_name=main_tab) # return to main search tab
                    
                    if time.time() - start > work_time_sec:
                        break
            except:
                print('article scraper failed')
            finally:
                self.browser.quit()
                scraper_status.status='FREE'
                scraper_status.save()

        else:
            print('scraper is busy')

