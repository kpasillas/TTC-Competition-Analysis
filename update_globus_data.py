#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import re
from datetime import datetime
from time import sleep
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
    
    today = datetime.today()
    file_name = 'globus_raw_data_{}.csv'.format(today.strftime("%m-%d-%y"))
    link_prefix = 'https://www.globusjourneys.com'
    regions_US = []
    trips_US = set()
    regions_AU = []
    trips = []
    error_log = dict()

    trip_countries = [
        {'country_name':'United States', 'US_link':'https://www.globusjourneys.com/tour/united-states/', 'AU_link':''},
        {'country_name':'Canada', 'US_link':'https://www.globusjourneys.com/tour/canada/', 'AU_link':''}
    ]

    def get_trip(url, retry_count=0):

        driver = webdriver.Chrome()
        driver.get(url)

        departures = []
        
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1')))
            sleep(1)
            years_dropdown = driver.find_element_by_class_name('dropdown')
            year_options = driver.find_elements_by_css_selector('option')
            num_of_years = len(year_options)

            trip_title_element = driver.find_element_by_css_selector('h1')
            trip_name = BeautifulSoup(trip_title_element.get_attribute('innerHTML'), 'lxml').text.strip()
            trip_code = 'Globus{}'.format(driver.find_element_by_class_name('dph__subtitle').find_element_by_class_name('text-secondary-dark').text)
            
            for year_num in range(num_of_years):
                sleep(1)
                years_dropdown = driver.find_element_by_class_name('dropdown')
                years_dropdown.click()
                sleep(1)
                year_options = driver.find_elements_by_css_selector('option')
                year_option = year_options[year_num]
                year_option.click()
                sleep(1)

                departure_elements = driver.find_elements_by_class_name('dapm__departures')
            
                for departure_element in departure_elements:
                
                    departure = BeautifulSoup(departure_element.get_attribute('innerHTML'), 'lxml')
                    date_numbers = departure.find('span', class_='dapm__date').text.split()
                    departure_date = '{:02}-{}-{}'.format(int(date_numbers[0]), date_numbers[1][:3], date_numbers[2])
                
                    if departure.find('div', class_='dapm__room-discount'):
                        actual_price_usd = departure.find('div', class_='dapm__room-discount').text.strip().replace(',', '').replace('$', '')
                    else:
                        actual_price_usd = ''
                    if departure.find('span', class_='dapm__room-price'):
                        original_price_usd = departure.find('span', class_='dapm__room-price').text.strip().replace(',', '').replace('$', '')
                    else:
                        original_price_usd = actual_price_usd
                
                    if departure.find('div', class_='small-group') and departure.find('div', class_='popular'):
                        type = 'Small-Group Discovery & Popular'
                    elif departure.find('div', class_='small-group'):
                        type = 'Small-Group Discovery'
                    elif departure.find('div', class_='popular'):
                        type = 'Popular'
                    else:
                        type = ''
                
                    if departure.find('div', class_='dapm__seat-counter'):
                        notes = departure.find('div', class_='dapm__seat-counter').text.strip()
                    else:
                        notes = ''

                    dep_columns = departure.find_all('div', class_='ng-star-inserted')

                    for dep_column in dep_columns:
                        if dep_column.text == ' sold out ':
                            status = 'Not Available'
                            available = False
                            break
                        else:
                            status = 'Available'
                            available = True
                    
                    new_dep = Departure(date = departure_date, actual_price_usd = actual_price_usd, original_price_usd = original_price_usd, type = type, notes = notes, status = status, available = available)
                    departures.append(new_dep)
            
            return Trip(trip_name, trip_code, departures)
        
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


    for country in tqdm(trip_countries):
        
        if country['US_link']:
            driver = webdriver.Chrome()
            driver.get(country['US_link'])
            
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'g-card__button')))
                regions = driver.find_elements_by_class_name('g-card__button')
                
                for region in regions:
                    soup = BeautifulSoup(region.get_attribute('outerHTML'), 'lxml')

                    if soup.find('a').get('href'):
                        link = '{}{}'.format(link_prefix, soup.find('a').get('href'))
                        regions_US.append(link)
                    
            finally:
                driver.quit()

    regions_US.append('https://www.globusjourneys.com/tour/south-america/')


    for region in tqdm(regions_US):
        
        driver = webdriver.Chrome()
        driver.get(region)
        
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'm-card__button')))
            tours = driver.find_elements_by_class_name('m-card__button')
            
            for tour in tours:
                soup = BeautifulSoup(tour.get_attribute('outerHTML'), 'lxml')
                links_soup = soup.find_all('a')

                for link_soup in links_soup:
                    full_link = link_soup.get('href').rsplit('/', 1)
                    link = '{}{}/dates-and-prices/{}'.format(link_prefix, full_link[0], full_link[1])
                    trips_US.add(link)
                
        except TimeoutException:
            error_log['{} - US'.format(region)] = 'Non-List of Trips'
            logger.debug('{} - US - Non-List of Trips'.format(region))
            
        finally:
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
    print('\n\n***           ***')

    print("\nGlobus, Done!\n")

if __name__ == '__main__': main()