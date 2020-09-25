#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import csv
import re
from datetime import datetime
from tqdm import tqdm
import time

def main():

    link_prefix = 'https://www.gocollette.com'
    today = datetime.now()
    file_name = 'collette_raw_data_{}.csv'.format(today.strftime("%m-%d-%y"))
    error_log = dict()
    trips_US = []
    trips_AU = []
    
    trip_continent = [
        {'region_name':'North America', 'US_link':'https://www.gocollette.com/en/find-your-tour#q/continentnames=North%20America&currentPage=1&sortDirection=desc&sortBy=', 'AU_link':'https://www.gocollette.com/en-au%2Ffind-your-tour%3Fsite%3Dcollette-au#q/continentnames=North%20America&currentPage=1&sortDirection=desc&sortBy='},
        {'region_name':'South America', 'US_link':'https://www.gocollette.com/en%2Ffind-your-tour%3Fsite%3Dcollette-us#q/continentnames=South%20America&currentPage=1&sortDirection=desc&sortBy=', 'AU_link':'https://www.gocollette.com/en-au/find-your-tour#q/continentnames=South%20America&currentPage=1&sortDirection=desc&sortBy='}
    ]

    with open(file_name, 'a') as new_file:
        csv_writer = csv.writer(new_file, lineterminator='\n')

        field_names = ['Trip Name','DepartureID','field','value']
        csv_writer.writerow(field_names)
        # print(field_names)

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

        for continent in trip_continent:

            driver = webdriver.Chrome()
            driver.get(continent['AU_link'])
            
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
                        
                        trips_AU.append({'trip_name':title, 'link':link})

            finally:
                driver.quit()
        
        # for Error Log
        # trips_US = [
        #     {'trip_name':'', 'link':''},
        #     {'trip_name':'', 'link':''},
        #     {'trip_name':'', 'link':''},
        # ]

        for trip in tqdm(trips_US):

            if trip['link']:

                previous_departure_date = ''
                duplicate_departure_count = 0
                
                driver = webdriver.Chrome()
                driver.get(trip['link'])

                nameElement = driver.find_element_by_tag_name('h3')
                soup = BeautifulSoup(nameElement.get_attribute('innerHTML'), 'lxml')

                op_code = trip['trip_name']
                trip_name = trip['trip_name']
                # trip_name = soup.contents[0].text.strip()
                # print(trip_name)

                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'date-group-dates')))

                    monthElements = driver.find_elements_by_class_name('date-group-dates')
                    for month in monthElements:

                        departureElements = month.find_elements_by_class_name('date-group')
                        for departure in departureElements:

                            soup = BeautifulSoup(departure.get_attribute('innerHTML'), 'lxml')

                            date_numbers = soup.find('div', class_='date').text.split()
                            departure_date = '{:02}-{}-{}'.format(int(date_numbers[1].strip(',')), date_numbers[0], date_numbers[2])
                            
                            if departure_date == previous_departure_date:                   # check if duplicate departure
                                duplicate_departure_count += 1
                            else:
                                duplicate_departure_count = 0

                            departure_letter = str(chr(duplicate_departure_count + 97))
                            day = '{:02}'.format(int(date_numbers[1].strip(',')))
                            month = str(chr((datetime.strptime(date_numbers[0], '%b')).month + 64))
                            year = '{}'.format(date_numbers[2][-2:])
                            departure_code = '{}{}{}{}'.format(day, month, year, departure_letter)
                            departure_id = departure_code                                   # no op_code available on website, need to add manually in format_data
                            # print(departure_id)

                            string_to_write = [trip_name,departure_id,'DepartureDate',departure_date]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)

                            if soup.find('div', class_='danger'):                           # check for 'Only x seats remaining'
                                status = 'Limited'
                                notes = soup.find('div', class_='danger').text.strip()
                                string_to_write = [trip_name,departure_id,'Notes',notes]
                                csv_writer.writerow(string_to_write)
                                # print(string_to_write)
                            elif soup.find('div', class_='date-alert'):                     # check if Cancelled, Guaranteed, or Sold Out
                                status = soup.find('div', class_='date-alert').text.strip()
                                if status == 'Call 800.340.5158 for details':
                                    notes = status
                                    string_to_write = [trip_name,departure_id,'Notes',notes]
                                    csv_writer.writerow(string_to_write)
                                    # print(string_to_write)
                                    status = 'Cancelled'
                                elif status == 'Guaranteed':
                                    type_guaranteed = status
                                    string_to_write = [trip_name,departure_id,'Type',type_guaranteed]
                                    csv_writer.writerow(string_to_write)
                                    # print(string_to_write)
                                    status = 'Available'
                                elif re.search( "Expires", status):
                                    notes = status
                                    string_to_write = [trip_name,departure_id,'Notes',notes]
                                    csv_writer.writerow(string_to_write)
                                    # print(string_to_write)
                                    status = 'Available'
                            else:
                                status = 'Available'
                            string_to_write = [trip_name,departure_id,'Status',status]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)
                            
                            if status == 'Cancelled' or status == 'Sold Out':
                                available = False
                            else:
                                available = True
                            string_to_write = [trip_name,departure_id,'Available',available]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)

                            actual_price = soup.find('span', class_='discountedPrice').text.strip().replace(',', '')
                            string_to_write = [trip_name,departure_id,'ActualPriceUSD',actual_price]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)

                            if soup.find('span', class_='crossout'):
                                original_price = soup.find('span', class_='crossout').text.strip().replace(',', '')
                            else:
                                original_price = actual_price
                            string_to_write = [trip_name,departure_id,'OriginalPriceUSD',original_price]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)

                            previous_departure_date = departure_date

                except TimeoutException:
                    error_log['{} - US'.format(op_code)] = 'Missing from Website'
                
                finally:
                    driver.quit()

            else:
                error_log['{} - US'.format(op_code)] = 'Missing US \'Book Now\' link'
            
        # for Error Log
        # trips_AU = [
        # {'trip_name':'', 'link':''},
        # {'trip_name':'', 'link':''},
        # {'trip_name':'', 'link':''},
        # ]

        for trip in tqdm(trips_AU):

            op_code = trip['trip_name']
            trip_name = trip['trip_name']

            if trip['link']:

                previous_departure_date = ''
                duplicate_departure_count = 0
                driver = webdriver.Chrome()
                driver.get(trip['link'])

                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'date-group-dates')))

                    monthElements = driver.find_elements_by_class_name('date-group-dates')
                    for month in monthElements:

                        departureElements = month.find_elements_by_class_name('date-group')
                        for departure in departureElements:

                            soup = BeautifulSoup(departure.get_attribute('innerHTML'), 'lxml')

                            date_numbers = soup.find('div', class_='date').text.split()
                            departure_date = '{:02}-{}-{}'.format(int(date_numbers[1].strip(',')), date_numbers[0], date_numbers[2])
                            # print(departure_date)

                            if departure_date == previous_departure_date:                   # check if duplicate departure
                                duplicate_departure_count += 1
                            else:
                                duplicate_departure_count = 0

                            departure_letter = str(chr(duplicate_departure_count + 97))
                            day = '{:02}'.format(int(date_numbers[1].strip(',')))
                            month = str(chr((datetime.strptime(date_numbers[0], '%b')).month + 64))
                            year = '{}'.format(date_numbers[2][-2:])
                            departure_code = '{}{}{}{}'.format(day, month, year, departure_letter)
                            departure_id = departure_code                                   # no op_code available on website, need to add manually in format_data
                            # print(departure_id)

                            actual_price = soup.find('span', class_='discountedPrice').text.strip().replace(',', '')
                            string_to_write = [trip_name,departure_id,'ActualPriceAUD',actual_price]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)

                            if soup.find('span', class_='crossout'):
                                original_price = soup.find('span', class_='crossout').text.strip().replace(',', '')
                            else:
                                original_price = actual_price
                            string_to_write = [trip_name,departure_id,'OriginalPriceAUD',original_price]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)

                            previous_departure_date = departure_date

                except TimeoutException:
                    error_log['{} - AU'.format(op_code)] = 'Missing from Website'
                
                finally:
                    driver.quit()

            else:
                error_log['{} - AU'.format(op_code)] = 'Missing AU \'Book Now\' link'

    print('\n\n*** Error Log ***')
    for code, error in error_log.items():
        print('{}: {}'.format(code, error))
    print('\n\n***           ***')
    
    print("\nDone!\n")

if __name__ == '__main__': main()