#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import re
import csv
from datetime import datetime

def main():

    today = datetime.today()
    file_name = 'cosmos_raw_data_{}.csv'.format(today.strftime("%m-%d-%y"))
    link_prefix = 'https://www.cosmos.com'
    regions_US = []
    trips_US = []
    regions_AU = []
    error_log = dict()

    trip_continents = [
        {'continent_name':'North America', 'US_link':'https://www.cosmos.com/Vacations/North-America/', 'AU_link':''}
    ]

    for continent in tqdm(trip_continents):

        if continent['US_link']:
            driver = webdriver.Chrome()
            driver.get(continent['US_link'])

            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'row')))
                region_rows = driver.find_elements_by_class_name('row')

                for region_row in region_rows:
                    soup = BeautifulSoup(region_row.get_attribute('innerHTML'), 'lxml')
                    regions = soup.find_all('a')

                    for region in regions:
                        link = '{}{}'.format(link_prefix, region.get('href'))
                        regions_US.append(link)

            finally:
                driver.quit()

    regions_US.append('https://www.cosmos.com/Vacations/South-America/')

    # print(regions_US)

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

        finally:
            driver.quit()

    # print(trips_US)

    for continent in tqdm(trip_continents):

        if continent['AU_link']:
            driver = webdriver.Chrome()
            driver.get(continent['AU_link'])

            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'destinations__item')))
                regions = driver.find_elements_by_class_name('destinations__item')

                for region in regions:    
                    soup = BeautifulSoup(region.get_attribute('innerHTML'), 'lxml')
                    link = soup.find('a').get('href')
                    regions_AU.append('{}.au{}'.format(link_prefix, link))

            finally:
                driver.quit()

    # print(regions_AU)

    with open(file_name, 'a') as new_file:
        csv_writer = csv.writer(new_file, lineterminator='\n')

        field_names = ['Trip Name','DepartureID','field','value']
        csv_writer.writerow(field_names)

        for trip in tqdm(trips_US):

            res = requests.get(trip['link'])
            soup = BeautifulSoup(res.text, 'lxml')

            try:
                trip_name = soup.find("h1").contents[0].text
                code = soup.find("h1").contents[2].text
                code = code.strip("()")
                # print('{} - {}'.format(trip_name, code))
                previous_departure_date = ''
                duplicate_departure_count = 0

                for departure in soup.find_all('div', class_='listing'):

                    date_numbers = departure.find('p', class_='date-numbers').text.split()
                    departure_date = '{:02}-{}-20{}'.format(int(date_numbers[0]), date_numbers[1], date_numbers[2])
                    # print(departure_date)

                    if departure_date == previous_departure_date:                   # check if duplicate departure
                        duplicate_departure_count += 1
                    else:
                        duplicate_departure_count = 0

                    departure_letter = str(chr(duplicate_departure_count + 97))
                    day = '{:02}'.format(int(date_numbers[0]))
                    month = str(chr((datetime.strptime(date_numbers[1], '%b')).month + 64))
                    year = date_numbers[2][-2:]
                    op_code = 'Cosmos{}{}'.format(code, year)
                    departure_code = '{}{}{}{}'.format(day, month, year, departure_letter)
                    departure_id = '{}-{}'.format(op_code, departure_code)
                    # print(departure_id)

                    string_to_write = [trip_name,departure_id,'DepartureDate',departure_date]
                    csv_writer.writerow(string_to_write)
                    # print(string_to_write)

                    actual_price = departure.find('p', class_='price-actual').text.strip().replace(',', '')
                    string_to_write = [trip_name, departure_id,'ActualPriceUSD',actual_price]
                    csv_writer.writerow(string_to_write)
                    # print(string_to_write)

                    if departure.find('p', class_='price-strike'):
                        original_price = departure.find('p', class_='price-strike').text.strip().replace(',', '')
                    else:
                        original_price = actual_price
                    string_to_write = [trip_name,departure_id,'OriginalPriceUSD',original_price]
                    csv_writer.writerow(string_to_write)
                    # print(string_to_write)

                    if departure.find('div', class_='small-message'):
                        type_smallgroup = 'Small-Group Discovery'
                        string_to_write = [trip_name,departure_id,'Type',type_smallgroup]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)
                    elif departure.find('div', class_='popular-message'):
                        type_popular = 'Popular'
                        string_to_write = [trip_name,departure_id,'Type',type_popular]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)

                    if departure.find('div', class_='listing-status'):
                        notes = departure.find('div', class_='listing-status').text.strip()
                    else:
                        notes = ''
                    string_to_write = [trip_name,departure_id,'Notes',notes]
                    csv_writer.writerow(string_to_write)
                    # print(string_to_write)

                    if re.search( "Not Available", departure.find('div', class_='listing-buttons-contain').text) or notes == '0 Seats Remaining':
                        available = False
                        status = 'Not Available'
                    else:
                        available = True
                        status = 'Available'
                    string_to_write = [trip_name,departure_id,'Available',available]
                    csv_writer.writerow(string_to_write)
                    # print(string_to_write)
                    string_to_write = [trip_name,departure_id,'Status',status]
                    csv_writer.writerow(string_to_write)
                    # print(string_to_write)

                    previous_departure_date = departure_date
            
            except:
                error_log['{} - US'.format(link)] = 'Missing from Website'

    print('\n\n*** Error Log ***')
    for code, error in error_log.items():
        print('{}: {}'.format(code, error))
    print('\n\n***           ***')

    print("\nDone!\n")

if __name__ == '__main__': main()