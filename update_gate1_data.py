#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import requests
import bs4
import csv
from datetime import date
from datetime import datetime
from tqdm import tqdm

from time import sleep

def main():

    today = date.today()
    file_name = 'gate1_raw_data_{}.csv'.format(today.strftime("%m-%d-%y"))
    link_prefix = 'https://www.gate1travel.com'
    regions_US = []
    trips_US = []
    regions_AU = []
    trips_set = set()
    error_log = dict()
    max_tries = 5

    trip_continent = [
        {'continent_name':'USA & Canada', 'US_link':'https://www.gate1travel.com/usa-canada?Brand=GATE1', 'AU_link':''},
        {'continent_name':'Latin America', 'US_link':'https://www.gate1travel.com/latin-america?Brand=GATE1', 'AU_link':''}
    ]

    for continent in tqdm(trip_continent):

        if continent['US_link']:

            res = requests.get(continent['US_link'])
            soup = bs4.BeautifulSoup(res.text, 'lxml')

            trip_regions = soup.find_all('div', class_='region-thumbnail')

            for region in trip_regions:

                title = region.text.strip()
                link = link_prefix + region.find('a')['href']
                regions_US.append({'region_name':title, 'region_link':link})



    # regions_US = [
    #     {'region_name':'Peru', 'region_link':'https://www.gate1travel.com/latin-america/peru?Brand=GATE1'},
    #     {'region_name':'National Parks', 'region_link':'https://www.gate1travel.com/usa-canada/usa?Brand=GATE1'}
    # ]



    for region in tqdm(regions_US):
        # print(region)
        driver = webdriver.Chrome()
        driver.get(region['region_link'])

        try:
            season_buttons = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'season-buttons-inner')))
            # season_buttons = driver.find_element_by_class_name('season-buttons-inner')
            seasons = season_buttons.find_elements_by_class_name('btn')
            # print(season_buttons)
            num_of_years = len(seasons)
            # print(num_of_years)
            
            # for season in season_buttons.find_elements_by_class_name('btn'):
            for year_num in range(num_of_years):
                # print('Year Num: {}'.format(year_num))
                sleep(2)
                # season = seasons[year_num]
                season_buttons = driver.find_element_by_class_name('season-buttons-inner')
                seasons = season_buttons.find_elements_by_class_name('btn')
                # print(seasons[year_num].text)
                sleep(2)
                # print('Before Click')
                seasons[year_num].click()
                
                region_panel = driver.find_elements_by_class_name('panel-body')
                num_of_regions = len(region_panel)
                # print('Num of Regions: {}'.format(num_of_regions))

                for region_num in range(num_of_regions):
                    # print('Region Num: {}'.format(region_num))
                    # sleep(2)
                    region_panel = driver.find_elements_by_class_name('panel-body')

                    trip_panels = region_panel[region_num].find_elements_by_class_name('Off-Season')
                    num_of_trips = len(trip_panels)
                    # print('Num of Trips: {}'.format(num_of_trips))

                    region_panel_soup = bs4.BeautifulSoup(region_panel[region_num].get_attribute('innerHTML'), 'lxml')
                    # print(region_panel_soup.prettify())

                    trip_panels_soup = region_panel_soup.find_all('li')
                    for trip in trip_panels_soup:
                        trip_name = trip.find('a').text
                        trip_link = link_prefix + trip.find('a').get('href')
                        trips_US.append({'trip_name':trip_name, 'trip_link':trip_link})

                sleep(2)

        finally:
            driver.quit()
    
    for trip in trips_US:
        trips_set.add(trip['trip_link'])
    # print(trips_set)

    with open(file_name, 'a') as new_file:
        csv_writer = csv.writer(new_file, lineterminator='\n')

        field_names = ['Trip Name','DepartureID','field','value']
        csv_writer.writerow(field_names)
    
        for link in tqdm(trips_set):

            res = get_html(link)
            # print(type(res))
            soup = bs4.BeautifulSoup(res.text, 'lxml')

            try:
                trip_name = soup.find("h2").text.strip()
                # print(trip_name)
                code = link.split('.')[-2].split('-')[-1].upper()
                op_code = 'Gate1{}'.format(code)
                # print(op_code)
                previous_departure_date = ''
                duplicate_departure_count = 0

                data_table = soup.find('table', class_='date-price-table')
                hidden_xs_items = data_table.find_all(class_='hidden-xs')
                # year = hidden_xs_items[0].text.split()[0][-2:]
                year = data_table.find('th').text.split()[0][-2:]
                
                for hidden_xs_item in hidden_xs_items:
                    table_rows = hidden_xs_item.find_all('tr')
                    for row in table_rows:

                        if row.find(class_='h4'):             # look for "YEAR Dates & Prices" if multiple years on same page
                            year = row.find('th').text.split()[0][-2:]
                        
                        elif row.get('class') == ['pricerow']:             # look for departure row
                            departure = row
                
                            if departure.find('del', class_='text-muted'):                          # check if date is crossed-off (Sold Out or Cancelled)
                                date_numbers = departure.find('del', class_='text-muted').text.split()
                                available = False
                            elif departure.find('button', class_='serviceDate'):
                                date_numbers = departure.find('button', class_='serviceDate').text.split()
                                available = True
                            
                            if len(date_numbers) == 3:                                                     # check if date format includes day of week
                                departure_date = '{}-{}-20{}'.format(date_numbers[2], date_numbers[1], year)
                                day = '{:02}'.format(int(date_numbers[2]))
                                month = str(chr((datetime.strptime(date_numbers[1], '%b')).month + 64))
                            else:
                                departure_date = '{}-{}-20{}'.format(date_numbers[1], date_numbers[0], year)
                                day = '{:02}'.format(int(date_numbers[1]))
                                month = str(chr((datetime.strptime(date_numbers[0], '%b')).month + 64))
                            # print(departure_date)

                            if departure_date == previous_departure_date:                   # check if duplicate departure
                                duplicate_departure_count += 1
                            else:
                                duplicate_departure_count = 0

                            departure_letter = str(chr(duplicate_departure_count + 97))
                            departure_code = '{}{}{}{}'.format(day, month, year, departure_letter)
                            departure_id = '{}-{}'.format(op_code, departure_code)
                            # print(departure_id)

                            string_to_write = [trip_name,departure_id,'DepartureDate',departure_date]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)
                            
                            string_to_write = [trip_name,departure_id,'Available',available]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)

                            if departure.find('span', class_='text-danger'):
                                notes = departure.find('span', class_='text-danger').text
                                if notes == '(Sold Out)':
                                    status = 'Sold Out'
                                else:                                                     # check if "Only x seats left!"
                                    status = 'Limited'
                            else:
                                notes = ''
                                if available == False:
                                    status = 'Cancelled'
                                else:
                                    status = 'Available'
                            string_to_write = [trip_name,departure_id,'Notes',notes]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)
                            string_to_write = [trip_name,departure_id,'Status',status]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)

                            if departure.find('td', class_='bookby-price'):
                                prices = departure.find_all('td', class_='text-center')
                                actual_price = prices[0].text.strip().strip('*').replace(',', '')
                                string_to_write = [trip_name,departure_id,'ActualPriceUSD',actual_price]
                                csv_writer.writerow(string_to_write)
                                # print(string_to_write)
                                original_price = prices[1].text.strip().strip('*').replace(',', '')
                                string_to_write = [trip_name,departure_id,'OriginalPriceUSD',original_price]
                                csv_writer.writerow(string_to_write)
                                # print(string_to_write)
                            else:
                                actual_price = departure.find('td', class_='text-center').text.strip().strip('*').replace(',', '')
                                string_to_write = [trip_name,departure_id,'ActualPriceUSD',actual_price]
                                csv_writer.writerow(string_to_write)
                                # print(string_to_write)
                                string_to_write = [trip_name,departure_id,'OriginalPriceUSD',actual_price]
                                csv_writer.writerow(string_to_write)
                                # print(string_to_write)
                            
                            previous_departure_date = departure_date

            except AttributeError:
                error_log['{} - US'.format(link)] = 'Missing from Website'
    
    print("\nDone!\n")


def get_html(url, retry_count=0):
    # print('In get_html')
    try:
        # print('In get_html -> try')
        res = requests.get(url)
        return res
    # except ConnectionResetError as e:
    except:
        print('Retry Count: {}'.format(retry_count))
        if retry_count >= 5:
            raise e
            # print('Error')
            # pass
        sleep(5)
        get_html(url, retry_count + 1)


if __name__ == '__main__': main()