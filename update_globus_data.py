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
    trips_US = []
    regions_AU = []
    trips = []
    error_log = dict()

    trip_countries = [
        {'continent_name':'United States', 'US_link':'https://www.globusjourneys.com/Vacation-Packages/Tour-United-States/', 'AU_link':''},
        {'continent_name':'Canada', 'US_link':'https://www.globusjourneys.com/Vacation-Packages/Tour-Canada/', 'AU_link':''}
    ]


    for country in tqdm(trip_countries):
        
        if country['US_link']:
            driver = webdriver.Chrome()
            driver.get(country['US_link'])
            
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'explore-dest')))
                regions = driver.find_elements_by_class_name('explore-dest')
                
                for region in regions:
                    soup = BeautifulSoup(region.get_attribute('innerHTML'), 'lxml')
                    link = '{}{}'.format(link_prefix, soup.find('a').get('href'))
                    regions_US.append(link)
                    
            finally:
                driver.quit()

    regions_US.append('https://www.globusjourneys.com/Vacation-Packages/Tour-South-America/Central-America/')
    regions_US.append('https://www.globusjourneys.com/Vacation-Packages/Tour-Cuba/Vacations/')


    for region in tqdm(regions_US):
        
        driver = webdriver.Chrome()
        driver.get(region)
        
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-list-contain')))
            tours = driver.find_elements_by_class_name('product-list-contain')
            
            for tour in tours:
                soup = BeautifulSoup(tour.get_attribute('innerHTML'), 'lxml')
                title = soup.find('h3').text.strip()
                link = '{}{}'.format(link_prefix, soup.find('div', class_='btn-red').find_parent('a').get('href'))
                trips_US.append({'trip_name':title, 'link':link})
                
        except TimeoutException:
            error_log['{} - US'.format(region)] = 'Non-List of Trips'
            logger.debug('{} - US - Non-List of Trips'.format(region))
            
        finally:
            driver.quit()


    for country in tqdm(trip_countries):
        
        if country['AU_link']:
            driver = webdriver.Chrome()
            driver.get(country['AU_link'])
            
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'destinations__item')))
                regions = driver.find_elements_by_class_name('destinations__item')
                
                for region in regions:    
                    soup = BeautifulSoup(region.get_attribute('innerHTML'), 'lxml')
                    link = soup.find('a').get('href')
                    regions_AU.append('{}.au{}'.format(link_prefix, link))
                    
            finally:
                driver.quit()


    for trip in tqdm(trips_US):
        
        departures = []
        
        res = requests.get(trip['link'])
        soup = BeautifulSoup(res.text, 'lxml')

        try:
            trip_name = soup.find("h1").contents[0].text
            trip_code = 'Globus{}'.format(soup.find("h1").contents[2].text.strip("()"))
            
            for departure in soup.find_all('div', class_='listing'):
                
                date_numbers = departure.find('p', class_='date-numbers').text.split()
                departure_date = '{:02}-{}-20{}'.format(int(date_numbers[0]), date_numbers[1], date_numbers[2])
                
                actual_price_usd = departure.find('p', class_='price-actual').text.strip().replace(',', '')
                if departure.find('p', class_='price-strike'):
                    original_price_usd = departure.find('p', class_='price-strike').text.strip().replace(',', '')
                else:
                    original_price_usd = actual_price_usd
                
                if departure.find('div', class_='small-message'):
                    type = 'Small-Group Discovery'
                elif departure.find('div', class_='popular-message'):
                    type = 'Popular'
                else:
                    type = ''
                
                if departure.find('div', class_='listing-status'):
                    notes = departure.find('div', class_='listing-status').text.strip()
                else:
                    notes = ''
                
                if re.search( "Not Available", departure.find('div', class_='listing-buttons-contain').text) or notes == '0 Seats Remaining':
                    status = 'Not Available'
                    available = False
                else:
                    status = 'Available'
                    available = True
                    
                new_dep = Departure(date = departure_date, actual_price_usd = actual_price_usd, original_price_usd = original_price_usd, type = type, notes = notes, status = status, available = available)
                departures.append(new_dep)
            
            new_trip = Trip(trip_name, trip_code, departures)
            trips.append(new_trip)
        
        except:
            error_log['{} - US'.format(link)] = 'Missing from Website'
            logger.debug('{} - US - Missing from Website'.format(link))

    for trip in trips:
        trip.print_deps(file_name)

    print('\n\n*** Error Log ***')
    for code, error in error_log.items():
        print('{}: {}'.format(code, error))
    print('\n\n***           ***')

    print("\nGlobus, Done!\n")

if __name__ == '__main__': main()