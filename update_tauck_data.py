#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import requests
import bs4
import re
import csv
from datetime import date
from datetime import datetime
from time import sleep
from tqdm import tqdm
import logging

from trip import Trip
from departure import Departure

def main():

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

    file_handler = logging.FileHandler(filename='update_competitor_data.log', mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    
    today = date.today()
    file_name = 'tauck_raw_data_{}.csv'.format(today.strftime("%m-%d-%y"))
    trips_US = set()
    trips = []
    error_log = dict()
    trip_list = []

    trip_regions = [
        {'region_name':'Canada', 'US_link':'https://www.tauck.com/tours-and-cruises/land-tours/canada-tours', 'AU_link':''},
        {'region_name':'United States', 'US_link':'https://www.tauck.com/tours-and-cruises/land-tours/united-states-land-tours', 'AU_link':''},
        {'region_name':'Latin America', 'US_link':'https://www.tauck.com/tours-and-cruises/land-tours/latin-america-land-tours', 'AU_link':''},
    ]

    def get_trip(url, retry_count=0):
        
        driver = webdriver.Chrome()
        driver.get(url)

        departures = []

        try:
            
            trip_name_element = driver.find_element_by_tag_name('h1')
            trip_name_soup = bs4.BeautifulSoup(trip_name_element.get_attribute('innerHTML'), 'lxml')
            trip_name = trip_name_soup.contents[0].text.strip()
            trip_code = 'Tauck{}'.format(link.split('=')[1][:-4].upper())
            
            trip_list.append(trip_name)

            years_holder_element = driver.find_element_by_class_name('c-search-filters__section__content__years')
            years_elements = years_holder_element.find_elements_by_tag_name('span')
            num_of_years = len(years_elements)
            datepicker_button_element = driver.find_element_by_class_name('c-btn-primary-b.datepicker__button.theme--light')

            for year_num in range(num_of_years):
                
                datepicker_button_element.click()
                sleep(1)
                year_element = driver.find_element_by_class_name('c-search-filters__section__content__years').find_elements_by_tag_name('span')[year_num]
                year_element.click()
                year = driver.find_element_by_class_name('c-search-filters__section__content__years').find_elements_by_tag_name('span')[year_num].text
                sleep(1)
                
                calendar_element = driver.find_element_by_class_name('sheet__data.ani-y.ani-timing-a.ani--in')
                departure_elements = calendar_element.find_elements_by_class_name('sheet__data__wrapper')
                
                for departure_element in departure_elements:
                    
                    departure_data = departure_element.find_elements_by_class_name('data-label')

                    date_numbers = departure_data[0].get_attribute('innerHTML').split()
                    departure_date = '{:02}-{}-{}'.format(int(date_numbers[1]), date_numbers[0], year)

                    if departure_data[2].get_attribute('innerHTML'):
                        type = departure_data[2].get_attribute('innerHTML')
                    else:
                        type = ''

                    actual_price_usd = departure_data[4].get_attribute('innerHTML').replace(',', '').replace('$', '').split()[0]

                    notes = departure_data[5].get_attribute('innerHTML')

                    if notes == 'Soldout':
                        status = 'Sold Out'
                        available = False
                    elif notes == 'Not Available':
                        status = 'Cancelled'
                        available = False
                    elif notes == 'Limited':
                        status = 'Limited'
                        available = True
                    elif notes == 'Available':
                        status = 'Available'
                        available = True
                    else:
                        status = 'UNRECOGNIZED STATUS'
                        available = False

                    new_dep = Departure(date = departure_date, actual_price_usd = actual_price_usd, type = type, notes = notes, status = status, available = available)
                    departures.append(new_dep)
                
                datepicker_button_element.click()

            new_trip = Trip(trip_name, trip_code, departures)
            trips.append(new_trip)

        except NoSuchElementException:
            error_log['{}'.format(url)] = 'Bad Link'
            logger.debug('{} - Bad Link'.format(url))

        except:
            driver.quit()

            if retry_count >= 5:
                error_log['{}'.format(url)] = 'Retry timeout'
                logger.debug('{} - Retry timeout'.format(url))
                return

            sleep(5)
            return get_trip(url, retry_count + 1)
        
        finally:
            driver.quit()


    for region in tqdm(trip_regions):

        if region['US_link']:
            driver = webdriver.Chrome()
            driver.get(region['US_link'])
            
            try:
                multiple_page_link_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'c-search-results-wrapper__pagination')))
                all_link_element = multiple_page_link_element.find_element_by_link_text('All')
                all_link_element.click()
                sleep(1)

            except TimeoutException:
                error_log['{} - US'.format(region)] = 'Non-List of Trips'
                logger.debug('{} - US - Non-List of Trips'.format(region))

            finally:
                trip_elements = (driver.find_element_by_class_name('js-search-results__content')).find_elements_by_class_name('c-search-result')

                for trip in trip_elements:
                    trip_title_element = trip.find_element_by_class_name('text-serif.title')
                    link = trip_title_element.get_attribute('href')
                    trips_US.add(link)

                driver.quit()


    # for Error Log
    # trips_US = (
    #     '',
    # )

    for trip in tqdm(trips_US):
        trips.append(get_trip(trip))


    for trip in trips:
        if trip is not None:
            trip.print_deps(file_name)
    
    print('\n\n*** Error Log ***')
    for code, error in error_log.items():
        print('{}: {}'.format(code, error))
    print('\n***           ***')

    print('\n\n*** List of Trips ***')
    for i in range(len(trip_list)):
        print('{}) {}'.format(i + 1, trip_list[i]))
        logger.info('{}) {}'.format(i + 1, trip_list[i]))
    print('\n\n***               ***')
    
    print("\nTauck, Done!\n")

if __name__ == '__main__': main()