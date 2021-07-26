#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
import requests
import bs4
from datetime import date
from datetime import datetime
from tqdm import tqdm
from time import sleep

from trip import Trip
from departure import Departure


def main():

    today = date.today()
    file_name = 'gate1_raw_data_{}.csv'.format(today.strftime("%m-%d-%y"))
    link_prefix = 'https://www.gate1travel.com'
    regions_US = []
    trips_US = []
    trips_set = set()
    trips = []
    error_log = dict()

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


    for region in tqdm(regions_US):

        driver = webdriver.Chrome()
        driver.get(region['region_link'])

        try:
            season_buttons = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'season-buttons-inner')))
            seasons = season_buttons.find_elements_by_class_name('btn')
            num_of_years = len(seasons)

            for year_num in range(num_of_years):

                try:
                    sleep(2)
                    season_buttons = driver.find_element_by_class_name('season-buttons-inner')
                    seasons = season_buttons.find_elements_by_class_name('btn')
                    sleep(2)
                    seasons[year_num].click()
                
                except ElementClickInterceptedException:
                    pass

                finally:
                    region_panel = driver.find_elements_by_class_name('panel-body')
                    num_of_regions = len(region_panel)

                    for region_num in range(num_of_regions):

                        region_panel = driver.find_elements_by_class_name('panel-body')
                        trip_panels = region_panel[region_num].find_elements_by_class_name('Off-Season')
                        region_panel_soup = bs4.BeautifulSoup(region_panel[region_num].get_attribute('innerHTML'), 'lxml')
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


    for link in tqdm(trips_set):

        departures = []
        
        res = get_html(link)
        soup = bs4.BeautifulSoup(res.text, 'lxml')

        try:
            trip_name = soup.find("h2").text.strip()
            trip_code = 'Gate1{}'.format(link.split('.')[-2].split('-')[-1].upper())
            
            data_table = soup.find('table', class_='date-price-table')
            hidden_xs_items = data_table.find_all(class_='hidden-xs')
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
                        else:
                            departure_date = '{}-{}-20{}'.format(date_numbers[1], date_numbers[0], year)
                            
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

                        if departure.find('td', class_='bookby-price'):
                            prices = departure.find_all('td', class_='text-center')
                            actual_price_usd = prices[0].text.strip().strip('*').replace(',', '')
                            original_price_usd = prices[1].text.strip().strip('*').replace(',', '')
                        else:
                            actual_price_usd = departure.find('td', class_='text-center').text.strip().strip('*').replace(',', '')
                            original_price_usd = actual_price_usd

                        new_dep = Departure(date = departure_date, actual_price_usd = actual_price_usd, original_price_usd = original_price_usd, notes = notes, status = status, available = available)
                        departures.append(new_dep)

            new_trip = Trip(trip_name, trip_code, departures)
            trips.append(new_trip)
            
            sleep(5)

        except AttributeError:
            error_log['{} - US'.format(link)] = 'Missing from Website'


    for trip in trips:
        trip.print_deps(file_name)


    print('\n\n*** Error Log ***')
    for code, error in error_log.items():
        print('{}: {}'.format(code, error))
    print('\n\n***           ***')


    print("\nDone!\n")


def get_html(url, retry_count=0):
    try:
        res = requests.get(url)
        return res
    # except ConnectionResetError as e:
    except:
        print('Retry Count: {}'.format(retry_count))
        if retry_count >= 10:
            raise e
            # print('Error')
            # pass
        sleep(10)
        return get_html(url, retry_count + 1)


if __name__ == '__main__': main()