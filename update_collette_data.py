#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
from datetime import datetime
import time

from trip import Trip
from departure import Departure


def main():

    today = datetime.now()
    file_name = 'collette_raw_data_{}.csv'.format(today.strftime("%m-%d-%y"))
    link_prefix = 'https://www.gocollette.com'
    trips_US = []
    trips_AU = []
    trips = []
    error_log = dict()
    
    trip_continent = [
        {'region_name':'North America', 'US_link':'https://www.gocollette.com/en/find-your-tour#q/continentnames=North%20America&currentPage=1&sortDirection=desc&sortBy=', 'AU_link':'https://www.gocollette.com/en-au%2Ffind-your-tour%3Fsite%3Dcollette-au#q/continentnames=North%20America&currentPage=1&sortDirection=desc&sortBy='},
        {'region_name':'South America', 'US_link':'https://www.gocollette.com/en%2Ffind-your-tour%3Fsite%3Dcollette-us#q/continentnames=South%20America&currentPage=1&sortDirection=desc&sortBy=', 'AU_link':'https://www.gocollette.com/en-au/find-your-tour#q/continentnames=South%20America&currentPage=1&sortDirection=desc&sortBy='}
    ]


    for continent in trip_continent:

        driver = webdriver.Chrome()
        driver.get(continent['US_link'])
        
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'tour-body')))
        
            while driver.find_element_by_class_name('grey_block_arrow').text:                       # check if 'VIEW MORE RESULTS' button present
                driver.find_element_by_class_name('grey_block_arrow').click()
                time.sleep(5)

            else:                                                                                   # all trips have been loaded
                tours = driver.find_elements_by_class_name('tour-body')
                
                for tour in tours:
                    
                    soup = BeautifulSoup(tour.get_attribute('innerHTML'), 'lxml')
                    
                    title = soup.find('h3', class_='tour-title').text.strip()

                    if soup.find('a', class_='bookNowButton'):
                        link = '{}{}'.format(link_prefix, soup.find('a', class_='bookNowButton').get('href'))
                    else:
                        link = ''
                    
                    trips_US.append({'trip_name':title, 'link':link})

        finally:
            driver.quit()
    
    # for Error Log
    # trips_US = [
    #     {'trip_name':'', 'link':''},
    # ]

    for trip in tqdm(trips_US):

        if trip['link']:

            departures = []

            driver = webdriver.Chrome()
            driver.get(trip['link'])

            nameElement = driver.find_element_by_tag_name('h3')
            soup = BeautifulSoup(nameElement.get_attribute('innerHTML'), 'lxml')

            trip_name = trip['trip_name']
            trip_code = trip['trip_name']

            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'date-group-dates')))

                monthElements = driver.find_elements_by_class_name('date-group-dates')
                for month in monthElements:

                    departureElements = month.find_elements_by_class_name('date-group')
                    for departure in departureElements:

                        soup = BeautifulSoup(departure.get_attribute('innerHTML'), 'lxml')

                        date_numbers = soup.find('div', class_='date').text.split()
                        departure_date = '{:02}-{}-{}'.format(int(date_numbers[1].strip(',')), date_numbers[0], date_numbers[2])
                        
                        if soup.find('div', class_='danger'):                           # check for 'Only x seats remaining'
                            notes = soup.find('div', class_='danger').text.strip()
                            status = 'Limited'
                            type = ''
                        elif soup.find('div', class_='date-alert'):                     # check if Cancelled, Guaranteed, or Sold Out
                            status = soup.find('div', class_='date-alert').text.strip()
                            if status == 'Call 800.340.5158 for details':
                                notes = status
                                status = 'Cancelled'
                                type = ''
                            elif status == 'Guaranteed':
                                notes = ''
                                type = status
                                status = 'Available'
                            elif re.search( "Expires", status):
                                notes = status
                                status = 'Available'
                                type = ''
                            else:
                                notes = ''
                                type = ''
                        else:
                            notes = ''
                            status = 'Available'
                            type = ''
                        
                        if status == 'Cancelled' or status == 'Sold Out':
                            available = False
                        else:
                            available = True
                        
                        actual_price_usd = soup.find('span', class_='discountedPrice').text.strip().replace(',', '')
                        
                        if soup.find('span', class_='crossout'):
                            original_price_usd = soup.find('span', class_='crossout').text.strip().replace(',', '')
                        else:
                            original_price_usd = actual_price_usd

                        new_dep = Departure(date = departure_date, actual_price_usd = actual_price_usd, original_price_usd = original_price_usd, type = type, notes = notes, status = status, available = available)
                        departures.append(new_dep)

            except TimeoutException:
                error_log['{} - US'.format(trip_code)] = 'Missing from Website'
            
            finally:
                driver.quit()

            new_trip = Trip(trip_name, trip_code, departures)
            trips.append(new_trip)

        else:
            error_log['{} - US'.format(trip['trip_name'])] = 'Missing US \'Book Now\' link'
        
    for trip in trips:
        trip.print_deps(file_name)
    
    print('\n\n*** Error Log ***')
    for code, error in error_log.items():
        print('{}: {}'.format(code, error))
    print('\n\n***           ***')
    
    print("\nDone!\n")

if __name__ == '__main__': main()