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

def main():

    today = date.today()
    file_name = 'tauck_raw_data_{}.csv'.format(today.strftime("%m-%d-%y"))
    trips_US = []
    error_log = dict()
    trip_list = []

    trip_regions = [
        {'region_name':'Canada', 'US_link':'https://www.tauck.com/tours-and-cruises/land-tours/canada-tours', 'AU_link':''},
        {'region_name':'United States', 'US_link':'https://www.tauck.com/tours-and-cruises/land-tours/united-states-land-tours', 'AU_link':''},
        {'region_name':'Latin America', 'US_link':'https://www.tauck.com/tours-and-cruises/land-tours/latin-america-land-tours', 'AU_link':''},
    ]

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
                pass

            finally:
                trip_elements = (driver.find_element_by_class_name('js-search-results__content')).find_elements_by_class_name('c-search-result')

                for trip in trip_elements:
                    trip_title_element = trip.find_element_by_class_name('text-serif.title')
                    title = bs4.BeautifulSoup(trip_title_element.get_attribute('innerHTML'), 'lxml').text.strip()
                    link = trip_title_element.get_attribute('href')
                    trips_US.append({'trip_name':title, 'link':link})

                driver.quit()

    # for Error Log
    # trips_US = [
    #     {'trip_name':'', 'link':''},
    # ]
    
    with open(file_name, 'a') as new_file:
        csv_writer = csv.writer(new_file, lineterminator='\n')

        field_names = ['Trip Name','DepartureID','field','value']
        csv_writer.writerow(field_names)

        for trip in tqdm(trips_US):

            driver = webdriver.Chrome()
            link = trip['link']
            driver.get(link)

            try:
                
                trip_name_element = driver.find_element_by_tag_name('h1')
                trip_name_soup = bs4.BeautifulSoup(trip_name_element.get_attribute('innerHTML'), 'lxml')
                trip_name = trip_name_soup.contents[0].text.strip()
                
                # print('{} - {}'.format(trip['trip_name'], trip['link']))
                trip_list.append(trip_name)
                
                code = link.split('=')[1][:-4].upper()
                # print(code)

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

                    op_code = 'Tauck{}{}'.format(code, year[-2:])
                    # print(op_code)
                    previous_departure_date = ''
                    duplicate_departure_count = 0        
                    
                    calendar_element = driver.find_element_by_class_name('sheet__data.ani-y.ani-timing-a.ani--in')
                    departure_elements = calendar_element.find_elements_by_class_name('sheet__data__wrapper')
                    
                    for departure_element in departure_elements:
                        
                        departure_data = departure_element.find_elements_by_class_name('data-label')

                        date_numbers = departure_data[0].get_attribute('innerHTML').split()
                        departure_date = '{:02}-{}-{}'.format(int(date_numbers[1]), date_numbers[0], year)
                        # print(departure_date)

                        if departure_date == previous_departure_date:                   # check if duplicate departure
                            duplicate_departure_count += 1
                        else:
                            duplicate_departure_count = 0
                        
                        departure_letter = str(chr(duplicate_departure_count + 97))
                        day = '{:02}'.format(int(date_numbers[1]))
                        month_letter = str(chr((datetime.strptime(date_numbers[0], '%b')).month + 64))
                        departure_code = '{}{}{}{}'.format(day, month_letter, year[-2:], departure_letter)
                        departure_id = '{}-{}'.format(op_code, departure_code)
                        # print(departure_id)

                        string_to_write = [trip_name,departure_id,'DepartureDate',departure_date]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)

                        if departure_data[2].get_attribute('innerHTML'):
                            departure_type = departure_data[2].get_attribute('innerHTML')
                            string_to_write = [trip_name,departure_id,'Type',departure_type]
                        else:
                            string_to_write = [trip_name,departure_id,'Type','Cruise']
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)

                        actual_price = departure_data[4].get_attribute('innerHTML').strip().replace(',', '')
                        string_to_write = [trip_name,departure_id,'ActualPriceUSD',actual_price]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)

                        notes = departure_data[5].get_attribute('innerHTML')
                        string_to_write = [trip_name,departure_id,'Notes',notes]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)

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
                        string_to_write = [trip_name,departure_id,'Status',status]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)
                        string_to_write = [trip_name,departure_id,'Available',available]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)

                        previous_departure_date = departure_date

                    datepicker_button_element.click()

            except StaleElementReferenceException:
                error_log['{} - {}'.format(trip_name, link)] = 'Error'
            
            finally:
                driver.quit()

    print('\n\n*** Error Log ***')
    for code, error in error_log.items():
        print('{}: {}'.format(code, error))
    print('\n***           ***')

    print('\n\n*** List of Trips ***')
    for i in range(len(trip_list)):
        print('{}) {}'.format(i + 1, trip_list[i]))
    print('\n\n***               ***')
    
    print("\nDone!\n")

if __name__ == '__main__': main()