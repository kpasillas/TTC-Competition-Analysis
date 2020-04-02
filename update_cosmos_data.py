#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import bs4
import re
import csv
from datetime import date
from datetime import datetime
from tqdm import tqdm

def main():

    today = date.today()
    file_name = 'cosmos_data_{}.csv'.format(today.strftime("%m-%d-%y"))

    error_log = dict()
    
    with open(file_name, 'a') as new_file:
        csv_writer = csv.writer(new_file, lineterminator='\n')

        field_names = ['Trip Name','DepartureID','Departure Date','field','value']
        csv_writer.writerow(field_names)

        linksUS = (
            'https://www.cosmos.com/tour/alaska-the-yukon/8360/?nextyear=true&content=price',       # Alaska & the Yukon
            'https://www.cosmos.com/tour/americas-greatest-treasure-with-rapid-city-start/8855/?nextyear=true&content=price',       # America's Greatest Treasure with Rapid City Start
            'https://www.cosmos.com/tour/atlantic-canadas-coastal-wonders/8820/?nextyear=true&content=price',       # Atlantic Canada's Coastal Wonders
            'https://www.cosmos.com/tour/brazil-argentina-chile-unveiled/1100/?nextyear=true&content=price',        # Brazil, Argentina & Chile Unveiled
            'https://www.cosmos.com/tour/brazil-argentina-chile-unveiled-with-peru/1105/?nextyear=true&content=price',      # Brazil, Argentina & Chile Unveiled with Peru
            'https://www.cosmos.com/tour/canadian-train-odyssey-with-alaska-cruise/8965/?nextyear=true&content=price',      # Canadian Train Odyssey with Alaska Cruise
            'https://www.cosmos.com/tour/canadian-train-odyssey/8960/?nextyear=true&content=price',     # Canadian Train Odyssey
            'https://www.cosmos.com/tour/circle-the-american-west/8160/?nextyear=true&content=price',       # Circle the American West
            'https://www.cosmos.com/tour/cities-of-the-great-east/8460/?nextyear=true&content=price',       # Cities of the Great East
            'https://www.cosmos.com/tour/classic-new-england-with-400th-mayflower-sailing/8105/?nextyear=true&content=price',       # Classic New England with 400th Mayflower Sailing
            'https://www.cosmos.com/tour/classic-new-england/8100/?nextyear=true&content=price',        # Classic New England
            'https://www.cosmos.com/tour/dixieland-rhythms/8240/?nextyear=true&content=price',      # Dixieland & Rhythms
            'https://www.cosmos.com/tour/eastern-us-canada-grand-vacation/8200/?nextyear=true&content=price',       # Eastern US & Canada Grand Vacation
            'https://www.cosmos.com/tour/exploring-americas-national-park/8620/?nextyear=true&content=price',       # Exploring America's National Park
            'https://www.cosmos.com/tour/exploring-the-eastern-seaboard/8310/?nextyear=true&content=price',     # Exploring the Eastern Seaboard
            'https://www.cosmos.com/tour/geysers-to-glaciers/8710/?nextyear=true&content=price',        # Geysers to Glaciers
            'https://www.cosmos.com/tour/golden-west-adventure/8500/?nextyear=true&content=price',      # Golden West Adventure
            'https://www.cosmos.com/tour/grand-alaskan-adventure/8420/?nextyear=true&content=price',        # Grand Alaskan Adventure
            'https://www.cosmos.com/tour/hawaiian-islands/8140/?nextyear=true&content=price',       # Hawaiian Islands
            'https://www.cosmos.com/tour/heart-of-the-canadian-rockies-with-alaska-cruise/8915/?nextyear=true&content=price',       # Heart of the Canadian Rockies with Alaska Cruise
            'https://www.cosmos.com/tour/heart-of-the-canadian-rockies-with-calgary-stampede/8550/?nextyear=true&content=price',        # Heart of the Canadian Rockies with Calgary Stampede
            'https://www.cosmos.com/tour/heart-of-the-canadian-rockies/8910/?nextyear=true&content=price',      # Heart of the Canadian Rockies
            'https://www.cosmos.com/tour/high-desert-discovery/8120/?nextyear=true&content=price',      # High Desert Discovery
            'https://www.cosmos.com/tour/highlights-of-route-66-with-mother-road-albuquerque-balloon-fiesta/8580/?nextyear=true&content=price',     # Highlights of Route 66 with Mother Road & Albuquerque Balloon Fiesta
            'https://www.cosmos.com/tour/highlights-of-route-66/8530/?nextyear=true&content=price',     # Highlights of Route 66
            'https://www.cosmos.com/tour/highlights-of-the-canyonlands/8520/?nextyear=true&content=price',      # Highlights of the Canyonlands
            'https://www.cosmos.com/tour/historic-trails-blue-ridge-mountains/8720/?nextyear=true&content=price',       # Historic Trails & Blue Ridge Mountains
            'https://www.cosmos.com/tour/mysteries-of-the-inca-empire/1300/?nextyear=true&content=price',       # Mysteries of the Inca Empire
            'https://www.cosmos.com/tour/national-parks-canyon-country-with-rapid-city-start/8605/?nextyear=true&content=price',        # National Parks & Canyon Country with Rapid City start
            'https://www.cosmos.com/tour/new-york-niagara-falls-washington-dc/8000/?nextyear=true&content=price',       # New York, Niagara Falls & Washington DC
            'https://www.cosmos.com/tour/ontario-french-canada/8330/?nextyear=true&content=price',      # Ontario & French Canada
            'https://www.cosmos.com/tour/rocky-mountain-discovery-with-rail/8630/?nextyear=true&content=price',     # Rocky Mountain Discovery with Rail
            'https://www.cosmos.com/tour/southern-sounds/8730/?nextyear=true&content=price',        # Southern Sounds
            'https://www.cosmos.com/tour/the-best-of-brazil-argentina/1000/?nextyear=true&content=price',       # The Best of Brazil & Argentina
            'https://www.cosmos.com/tour/the-canadian-rockies-with-alaska-cruise/8904/?nextyear=true&content=price',        # The Canadian Rockies with Alaska Cruise
            'https://www.cosmos.com/tour/the-canadian-rockies/8900/?nextyear=true&content=price',       # The Canadian Rockies
            'https://www.cosmos.com/tour/the-lone-star-state-to-the-french-quarter/8090/?nextyear=true&content=price',      # The Lone Star State to the French Quarter
            'https://www.cosmos.com/tour/the-old-south-florida/8290/?nextyear=true&content=price',      # The Old South & Florida
            'https://www.cosmos.com/tour/ultimate-south-america/1200/?nextyear=true&content=price',     # Ultimate South America
            'https://www.cosmos.com/tour/via-rail-and-the-canadian-rockies/8935/?nextyear=true&content=price',      # VIA Rail and the Canadian Rockies
            'https://www.cosmos.com/tour/via-rail-and-the-canadian-rockies-with-alaska-cruise/8940/?nextyear=true&content=price',       # VIA Rail and the Canadian Rockies with Alaska Cruise
            'https://www.cosmos.com/tour/via-rail-and-the-canadian-rockies-with-calgary-stampede/8470/?nextyear=true&content=price',        # VIA Rail and the Canadian Rockies with Calgary Stampede
            'https://www.cosmos.com/tour/western-canada-by-rail-with-alaska-cruise/8934/?nextyear=true&content=price',      # Western Canada by Rail with Alaska Cruise
            'https://www.cosmos.com/tour/western-canada-by-rail/8930/?nextyear=true&content=price',     # Western Canada by Rail
            'https://www.cosmos.com/tour/western-canada-with-inside-passage-calgary-stampede/8385/?nextyear=true&content=price',        # Western Canada with Inside Passage & Calgary Stampede
            'https://www.cosmos.com/tour/western-canada-with-inside-passage/8380/?nextyear=true&content=price',     # Western Canada with Inside Passage
            'https://www.cosmos.com/tour/western-wonders/8510/?nextyear=true&content=price'     # Western Wonders
        )

        print()

        for link in tqdm(linksUS):

            res = requests.get(link)
            soup = bs4.BeautifulSoup(res.text, 'lxml')

            trip_name = soup.find("h1").contents[0].text
            code = soup.find("h1").contents[2].text
            code = code.strip("()")
            op_code = 'Cosmos{}20'.format(code)
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
                departure_code = '{}{}{}{}'.format(day, month, year, departure_letter)
                departure_id = '{}-{}'.format(op_code, departure_code)
                # print(departure_id)
                
                actual_price = departure.find('p', class_='price-actual').text.strip().replace(',', '')
                string_to_write = [trip_name, departure_id,departure_date,'ActualPriceUSD',actual_price]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)
                
                if departure.find('p', class_='price-strike'):
                    original_price = departure.find('p', class_='price-strike').text.strip().replace(',', '')
                else:
                    original_price = actual_price
                string_to_write = [trip_name,departure_id,departure_date,'OriginalPriceUSD',original_price]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)
                
                if departure.find('div', class_='popular-message'):
                    popular_departure = True
                else:
                    popular_departure = False
                string_to_write = [trip_name,departure_id,departure_date,'Popular Departure',popular_departure]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)
                
                listing_status = departure.find('div', class_='listing-status').text.strip()
                string_to_write = [trip_name,departure_id,departure_date,'Listing Status',listing_status]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)
                
                if re.search( "Not Available", departure.find('div', class_='listing-buttons-contain').text):
                    available = False
                else:
                    available = True
                string_to_write = [trip_name,departure_id,departure_date,'Available',available]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)

                previous_departure_date = departure_date

            linkAU = "https://www.cosmostours.com.au/booking?tour={}&season=2020".format(code)
            driver = webdriver.Chrome()
            driver.get(linkAU)
            previous_departure_date = ''
            duplicate_departure_count = 0
            
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'booking-departures__wrapper')))

                departureElements = driver.find_elements_by_class_name('booking-departures__wrapper')
                for departure in departureElements:

                    soup = bs4.BeautifulSoup(departure.get_attribute('innerHTML'), 'lxml')

                    date_numbers = soup.find('span', class_='booking-departures__date').text.split()
                    departure_date = "{:02}-{}-{}".format(int(date_numbers[0]), (date_numbers[1])[0:3], date_numbers[2])
                    # print(departure_date)

                    if departure_date == previous_departure_date:                   # check if duplicate departure
                        duplicate_departure_count += 1
                    else:
                        duplicate_departure_count = 0

                    departure_letter = str(chr(duplicate_departure_count + 97))
                    day = '{:02}'.format(int(date_numbers[0]))
                    month = str(chr((datetime.strptime(date_numbers[1], '%B')).month + 64))
                    year = date_numbers[2][-2:]
                    departure_code = '{}{}{}{}'.format(day, month, year, departure_letter)
                    departure_id = '{}-{}'.format(op_code, departure_code)
                    # print(departure_id)

                    actual_price = soup.find('span', class_='booking-departures__price--amount').text.strip().replace(',', '')
                    string_to_write = [trip_name, departure_id,departure_date,'ActualPriceAUD',actual_price]
                    csv_writer.writerow(string_to_write)
                    # print(string_to_write)
                
                    if soup.find('span', class_='booking-departures__price--strike-through'):
                        original_price = soup.find('span', class_='booking-departures__price--strike-through').text.strip().replace(',', '')
                    else:
                        original_price = actual_price
                    string_to_write = [trip_name, departure_id,departure_date,'OriginalPriceAUD',original_price]
                    csv_writer.writerow(string_to_write)
                    # print(string_to_write)

                    previous_departure_date = departure_date

            except TimeoutException:
                error_log['{} - AU'.format(op_code)] = 'Missing from Website'
            
            finally:
                driver.quit()

        print('\n\n*** Error Log ***')
        for code, error in error_log.items():
            print('{}: {}'.format(code, error))
        
        print("\nDone!\n")

if __name__ == '__main__': main()